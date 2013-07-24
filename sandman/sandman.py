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

def _validate(cls, method, resource=None):
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

def resource_created_response(resource):
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
    """Return the appropriate *Response* with status code *403*, signaling the HTTP method used
    in the request is not supported for the given endpoint.
    
    :rtype: :class:`flask.Response`

    """
    response = Response()
    response.status_code = 403
    return response

def no_content_response():
    """Return the appropriate *Response* with status code *204*, signaling a completed action
    which does not require data in the response body
    
    :rtype: :class:`flask.Response`
    """
    response = Response()
    response.status_code = 204
    return response

@app.route('/<collection>/<lookup_id>', methods=['PATCH'])
def patch_resource(collection, lookup_id):
    """Return the appropriate *Response* based on action performed by HTTP PATCH request.
    
    If no resource currently exists at `/<collection>/<lookup_id>`, create it
    with *lookup_id* as its primary key and return a
    :func:`resource_created_response`.

    If a resource *does* exist at `/<collection>/<lookup_id>`, update it with
    the data sent in the request and return a :func:`no_content_response`.

    Note: HTTP `PATCH` (and, thus, :func:`patch_resource`) is idempotent

    :param string collection: a :class:`sandman.model.Resource` endpoint
    :param string lookup_id: the primary key for the associated :class:`sandman.model.Resource`
    :rtype: :class:`flask.Response`

    """
    session = _get_session()
    with app.app_context():
        cls = current_app.endpoint_classes[collection]

    resource = session.query(cls).get(lookup_id)

    if not _validate(cls, request.method, resource):
        return unsupported_method_response()

    if resource is None:
        resource = cls()
        resource.from_dict(request.json)
        setattr(resource, resource.primary_key(), lookup_id)
        session.add(resource)
        session.commit()
        return resource_created_response(resource)
    else:
        resource.from_dict(request.json)
        session.merge(resource)
        session.commit()
        return no_content_response()


@app.route('/<collection>', methods=['POST'])
def add_resource(collection):
    """Return the appropriate *Response* based on adding a new resource to *collection*

    :param string collection: a :class:`sandman.model.Resource` endpoint
    :rtype: :class:`flask.Response`

    """
    with app.app_context():
        cls = current_app.endpoint_classes[collection]
    resource = cls()
    resource.from_dict(request.json)

    if not _validate(cls, request.method, resource):
        return unsupported_method_response()

    session = _get_session()
    session.add(resource)
    session.commit()
    return resource_created_response(resource)

@app.route('/<collection>/<lookup_id>', methods=['DELETE'])
def delete_resource(collection, lookup_id):
    """Return the appropriate *Response* for deleting an existing resource in *collection*
    
    :param string collection: a :class:`sandman.model.Resource` endpoint
    :param string lookup_id: the primary key for the associated :class:`sandman.model.Resource`
    :rtype: :class:`flask.Response`

    """
    with app.app_context():
        cls = current_app.endpoint_classes[collection]
    resource = cls()
    session = _get_session()
    resource = session.query(cls).get(lookup_id)

    if resource is None:
        return JSONException('Requested resource not found', code=404)
    elif not _validate(cls, request.method, resource):
        return unsupported_method_response()

    session.delete(resource)
    session.commit()
    return no_content_response()


@app.route('/<collection>/<lookup_id>', methods=['GET'])
def resource_handler(collection, lookup_id):
    """Return the appropriate *Response* for retrieving a single resource
    
    :param string collection: a :class:`sandman.model.Resource` endpoint
    :param string lookup_id: the primary key for the associated :class:`sandman.model.Resource`
    :rtype: :class:`flask.Response`

    """
    session = _get_session()
    with app.app_context():
        cls = current_app.endpoint_classes[collection]
    resource = session.query(cls).get(lookup_id)

    if resource is None:
        return JSONException('Requested resource not found', code=404)
    elif not _validate(cls, request.method, resource):
        return unsupported_method_response()

    result_dict = resource.as_dict()
    return jsonify(**result_dict)

@app.route('/<collection>', methods=['GET'])
def collection_handler(collection):
    """Return the appropriate *Response* for retrieving a collection of resources
    
    :param string collection: a :class:`sandman.model.Resource` endpoint
    :param string lookup_id: the primary key for the associated :class:`sandman.model.Resource`
    :rtype: :class:`flask.Response`

    """
    with app.app_context():
        cls = current_app.endpoint_classes[collection]
    session = _get_session()
    resources = session.query(cls).all()

    if not _validate(cls, request.method, resources):
        return unsupported_method_response()

    result_list = []
    for resource in resources:
        result_list.append(resource.as_dict())
    return jsonify(resources=result_list)
