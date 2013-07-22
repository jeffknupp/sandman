"""Sandman REST API creator for Flask and SQLAlchemy"""

from flask import jsonify, request, g, current_app
from . import app, Session
from .exception import JSONException

def register(class_tuple):
    """Register an endpoint with the Model class that represents it"""
    with app.app_context():
        if getattr(current_app, 'endpoint_classes', None) is None:
            current_app.endpoint_classes = {}
        current_app.endpoint_classes[class_tuple[0]] = class_tuple[1]

def created_response(resource):
    """Return response for created resource"""
    response = jsonify(resource.as_dict())
    response.code = 201
    response.headers['Location']  = 'http://localhost:5000/' + resource.resource_uri()
    return response

@app.route('/<collection>', methods=['POST'])
def add_resource(collection):
    """Return response for adding a resource"""
    with app.app_context():
        cls = current_app.endpoint_classes[collection]
    resource = cls()
    resource.from_dict(request.json)
    session = Session()
    session.add(resource)
    session.commit()
    return created_response(resource)

@app.route('/<collection>/<lookup_id>', methods=['GET'])
def resource_handler(collection, lookup_id):
    """Handler for single resource"""
    session = Session()
    with app.app_context():
        cls = current_app.endpoint_classes[collection]
    print cls, lookup_id
    resource = session.query(cls).get(lookup_id)
    if resource is None:
        return JSONException('Requested resource not found', code=404)
    result_dict = resource.as_dict()
    return jsonify(**result_dict)

@app.route('/<collection>', methods=['GET'])
def collection_handler(collection):
    """Handler for a collection of resources"""
    print 'here'
    with app.app_context():
        cls = current_app.endpoint_classes[collection]
    session = Session()
    resources = session.query(cls).all()
    result_list = []
    for resource in resources:
        result_list.append(resource.as_dict())
    return jsonify(resources=result_list)
