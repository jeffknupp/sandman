"""Sandman REST API creator for Flask and SQLAlchemy"""

from flask import current_app, abort, jsonify, request
from sqlalchemy.orm import sessionmaker
from exception import JSONException


class Sandman(object):
    def __init__(self, app=None, db=None, models=None):
        self.app = app
        self.db = db
        self.models = models
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.add_url_rule("/<collection>", 'show_collection', collection_handler, methods=['GET'])
        app.add_url_rule("/<collection>", 'add_resource', add_resource, methods=['POST'])
        app.add_url_rule("/<collection>/<lookup_id>", 'show_resource', resource_handler, methods=['GET'])

    def get_endpoint_class(self, collection):
        return self.models[collection]

    
def created_response(self, resource):
    response = jsonify(resource.as_dict())
    response.code = 201
    response.headers['Location']  = 'http://localhost:5000/' + resource.resource_uri()
    return response

def add_resource(collection):
    cls = sandman.get_endpoint_class(collection)
    resource = cls()
    resource.from_dict(request.json)
    session = Session()
    session.add(resource)
    session.commit()
    return created_response(resource)

def resource_handler(collection, lookup_id):
    """Handler for single resource"""
    session = Session()
    cls = sandman.get_endpoint_class(collection)
    print cls, lookup_id
    resource = session.query(cls).get(lookup_id)
    if resource is None:
        return JSONException('Requested resource not found', code=404)
    result_dict = resource.as_dict()
    return jsonify(**result_dict)

def collection_handler(collection):
    """Handler for a collection of resources"""
    print 'here'
    cls = sandman.get_endpoint_class(collection)
    session = Session()
    resources = session.query(cls).all()
    result_list = []
    for resource in resources:
        result_list.append(resource.as_dict())
    return jsonify(resources=result_list)
