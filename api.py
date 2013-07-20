"""REST API for DMF"""

from flask import Flask, abort, jsonify, request
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base, DeferredReflection
from sqlalchemy.orm import sessionmaker
from werkzeug.exceptions import HTTPException

Base = declarative_base(cls=DeferredReflection)


class JSONException(HTTPException):
    def __init__(self, description=None, code=400, response=None):
        super(JSONException, self).__init__(description, response)
        self.code = code

    def get_headers():
        return [{'Content-type': 'application/json'}]

    def get_body():
        return jsonify({'result': False,
            'message': self.message})

class DictMixin(object):
    def as_dict(self):
        result_dict = {}
        for column in self.__table__.columns.keys():
            result_dict[column] = getattr(self, column, None)
        result_dict['links'] = self.links()
        return result_dict

    def from_dict(self, dictionary):
        for column in self.__table__.columns.keys():
            value = dictionary.get(column, None)
            setattr(self, column, value)
        
class Resource(DictMixin):
    def resource_uri(self):
        return '/{}/{}'.format(self.endpoint, self.primary_key())

    def links(self):
        """Get a list of links for possible actions on this resource"""
        links = []
        links.append({'rel': 'self', 'uri': self.resource_uri()})
        return links


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
    endpoing = 'jobDependencies'

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
