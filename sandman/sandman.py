"""Sandman REST API creator for Flask and SQLAlchemy"""

from flask import jsonify, request, g, current_app, Response
from . import app, db
from .exception import JSONException

def _get_session():
    """Return (and memoize) a database session"""
    session = getattr(g, '_session', None)
    if session is None:
        session = g._session = db.session()
    return session

def validate(cls, method, resource=None):
    """Return ``True`` if the the given *cls* supports the HTTP *method* found 
    on the incoming HTTP request.
    
    :param cls: class associated with the request's endpoint
    :type cls: :class:`sandman.model.Resource` instance
    :param string method: HTTP method of incoming request
    :param resource: *cls* instance associated with the request
    :type resource: :class:`sandman.model.Resource` or None
    :rtype: bool

    """
    if not method in cls.__methods__:
        return False

    class_validator_name = 'do_' + method

    if hasattr(cls, class_validator_name):
        class_validator = getattr(cls, class_validator_name)
        return class_validator(resource)

    return True

def created_response(resource):
    """Return HTTP response with status code *201*, signaling a created *resource*
    
    :param resource: resource created as a result of current request
    :type resource: :class:`sandman.model.Resource`
    :rtype: :class:`flask.Response`
    """
    response = jsonify(resource.as_dict())
    response.status_code = 201
    response.headers['Location']  = 'http://localhost:5000/' + resource.resource_uri()
    return response

def unsupported_method_response():
    """Return response when no resource is returned in body"""
    response = Response()
    response.status_code = 403
    return response

def no_content_response():
    """Return response when no resource is returned in body"""
    response = Response()
    response.status_code = 204
    return response

@app.route('/<collection>/<lookup_id>', methods=['PATCH'])
def patch_resource(collection, lookup_id):
    """Return response for patching a resource"""
    session = _get_session()
    with app.app_context():
        cls = current_app.endpoint_classes[collection]

    resource = session.query(cls).get(lookup_id)

    if not validate(cls, request.method, resource):
        return unsupported_method_response()

    if resource is None:
        resource = cls()
        resource.from_dict(request.json)
        setattr(resource, resource.primary_key(), lookup_id)
        session.add(resource)
        session.commit()
        return created_response(resource)
    else:
        resource.from_dict(request.json)
        updated_resource = session.merge(resource)
        session.commit()
        return no_content_response()


@app.route('/<collection>', methods=['POST'])
def add_resource(collection):
    """Return response for adding a resource"""
    with app.app_context():
        cls = current_app.endpoint_classes[collection]
    resource = cls()
    resource.from_dict(request.json)

    if not validate(cls, request.method, resource):
        return unsupported_method_response()

    session = _get_session()
    session.add(resource)
    session.commit()
    return created_response(resource)

@app.route('/<collection>/<lookup_id>', methods=['DELETE'])
def delete_resource(collection, lookup_id):
    """Return response for deleting a resource"""
    with app.app_context():
        cls = current_app.endpoint_classes[collection]
    resource = cls()
    session = _get_session()
    resource = session.query(cls).get(lookup_id)

    if resource is None:
        return JSONException('Requested resource not found', code=404)
    elif not validate(cls, request.method, resource):
        return unsupported_method_response()

    session.delete(resource)
    session.commit()
    return no_content_response()


@app.route('/<collection>/<lookup_id>', methods=['GET'])
def resource_handler(collection, lookup_id):
    """Handler for single resource"""
    session = _get_session()
    with app.app_context():
        cls = current_app.endpoint_classes[collection]
    resource = session.query(cls).get(lookup_id)

    if resource is None:
        return JSONException('Requested resource not found', code=404)
    elif not validate(cls, request.method, resource):
        return unsupported_method_response()

    result_dict = resource.as_dict()
    return jsonify(**result_dict)

@app.route('/<collection>', methods=['GET'])
def collection_handler(collection):
    """Handler for a collection of resources"""
    with app.app_context():
        cls = current_app.endpoint_classes[collection]
    session = _get_session()
    resources = session.query(cls).all()

    if not validate(cls, request.method, resources):
        return unsupported_method_response()

    result_list = []
    for resource in resources:
        result_list.append(resource.as_dict())
    return jsonify(resources=result_list)
