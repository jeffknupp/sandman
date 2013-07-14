"""Sandman REST API creator for Flask and SQLAlchemy"""

from flask import Flask, abort, jsonify, request
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from exception import JSONException


class Job(Base, Resource):
    """Job definition"""
    __tablename__ = 'new_job'
    endpoint = 'job'

    def primary_key(self):
        """Return value of primary key field."""
        return self.name
 
class JobScheduleInfo(Base, Resource):
    """Scheduling information for a particular job"""
    __tablename__ = 'job_schedule'
    endpoint = 'jobScheduleInfo'

    def primary_key(self):
        """Return value of primary key field."""
        return self.id

class JobDependencies(Base, Resource):
    """Dependency information for a particular job"""
    __tablename__ = 'job_schedule_rule'
    endpoint = 'jobDependencies'

    def primary_key(self):
        """Return value of primary key field."""
        return self.id


def created_response(resource):
    response = jsonify(resource.as_dict())
    response.code = 201
    response.headers['Location']  = 'http://localhost:5000/' + resource.resource_uri()
    return response

app = Flask(__name__)

@app.route("/<collection>", methods=['POST'])
def add_resource(collection):
    cls = get_endpoint_class(collection)
    resource = cls()
    resource.from_dict(request.json)
    session = Session()
    session.add(resource)
    session.commit()
    return created_response(resource)

@app.route("/<collection>/<lookup_id>", methods=['GET'])
def resource_handler(collection, lookup_id):
    """Handler for single resource"""
    session = Session()
    cls = get_endpoint_class(collection)
    print cls, lookup_id
    resource = session.query(cls).get(lookup_id)
    if resource is None:
        return JSONException('Requested resource not found', code=404)
    result_dict = resource.as_dict()
    return jsonify(**result_dict)

@app.route("/<collection>")
def collection_handler(collection):
    """Handler for a collection of resources"""
    cls = get_endpoint_class(collection)
    session = Session()
    resources = session.query(cls).all()
    result_list = []
    for resource in resources:
        result_list.append(resource.as_dict())
    return jsonify(resources=result_list)


    
def get_endpoint_class(endpoint):
    """Get mapping of endpoint to class names"""
    endpoint_classes = {'job': Job, 
            'jobScheduleInfo': JobScheduleInfo, 
            'jobDependencies': JobDependencies,
            }
    return endpoint_classes[endpoint]

if __name__ == "__main__":
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dmf'
    db = SQLAlchemy(app)
    Base.prepare(db.engine)
    Session = sessionmaker(db.engine)
    app.run(debug=True)
