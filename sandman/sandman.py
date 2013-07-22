"""Sandman REST API creator for Flask and SQLAlchemy"""

from flask import jsonify, request, g, current_app
from . import app, db
from sqlalchemy.orm import sessionmaker
from .exception import JSONException

def get_session():
    """Return a database session"""
    session = getattr(g, '_session', None)
    if session is None:
        session = g._session = sessionmaker(db.engine)()
    return session

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
    session = get_session()
    session.add(resource)
    session.commit()
    return created_response(resource)

@app.route('/<collection>/<lookup_id>', methods=['GET'])
def resource_handler(collection, lookup_id):
    """Handler for single resource"""
    session = get_session()
    with app.app_context():
        cls = current_app.endpoint_classes[collection]
    resource = session.query(cls).get(lookup_id)
    if resource is None:
        return JSONException('Requested resource not found', code=404)
    result_dict = resource.as_dict()
    return jsonify(**result_dict)

@app.route('/<collection>', methods=['GET'])
def collection_handler(collection):
    """Handler for a collection of resources"""
    with app.app_context():
        cls = current_app.endpoint_classes[collection]
    session = get_session()
    resources = session.query(cls).all()
    result_list = []
    for resource in resources:
        result_list.append(resource.as_dict())
    return jsonify(resources=result_list)
