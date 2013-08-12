"""Sandman REST API creator for Flask and SQLAlchemy"""

from flask import (jsonify, request, g, 
        current_app, Response, render_template,
        make_response)
from sqlalchemy.exc import IntegrityError
from . import app, db
from .exception import JSONException

JSON, HTML = range(2)

def _get_session():
    """Return (and memoize) a database session"""
    session = getattr(g, '_session', None)
    if session is None:
        session = g._session = db.session()
    return session

def _get_mimetype(current_request):
    """Return the mimetype for this request."""
    if 'Accept' not in current_request.headers:
        return JSON

    if 'json' in current_request.headers['Accept']:
        return JSON
    else:
        return HTML

def _single_resource_json_response(resource):
    """Return the JSON representation of *resource*"""
    return jsonify(**resource.as_dict())
   
def _single_resource_html_response(resource):
    """Return the HTML representation of *resource*"""
    tablename = resource.__tablename__
    resource.pk = getattr(resource, resource.primary_key())
    resource.attributes = resource.as_dict()
    return make_response(render_template('resource.html', resource=resource,
        tablename=tablename))

def _collection_json_response(resources):
    """Return the HTML representation of the collection *resources*"""
    result_list = []
    for resource in resources:
        result_list.append(resource.as_dict())
    return jsonify(dict(result_list))

def _collection_html_response(resources):
    """Return the HTML representation of the collection *resources*"""
    return make_response(render_template('collection.html',
        resources=resources))

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

    class_validator_name = 'validate_' + method

    if hasattr(cls, class_validator_name):
        class_validator = getattr(cls, class_validator_name)
        return class_validator(resource)

    return True

def endpoint_class(collection):
    """Return the :class:`sandman.model.Resource` associated with the endpoint
    *collection*.

    :param string collection: a :class:`sandman.model.Resource` endpoint
    :rtype: :class:`sandman.model.Resource`

    """
    session = _get_session()
    with app.app_context():
        return current_app.endpoint_classes[collection]

def retrieve_resource(collection, key):
    """Return the resource of type *cls* identified by key *key*.

    :param string collection: a :class:`sandman.model.Resource` endpoint
    :param string key: primary key of resource
    :rtype: class:`sandman.model.Resource`
    """
    session = _get_session()
    with app.app_context():
        cls = current_app.endpoint_classes[collection]
    return session.query(cls).get(key)

def resource_created_response(resource, current_request):
    """Return HTTP response with status code *201*, signaling a created *resource*
    
    :param resource: resource created as a result of current request
    :type resource: :class:`sandman.model.Resource`
    :rtype: :class:`flask.Response`
    """
    if _get_mimetype(current_request) == JSON:
        response = _single_resource_json_response(resource)
    else:
        response = _single_resource_html_response(resource)
    response.status_code = 201
    response.headers['Location']  = 'http://localhost:5000/' + resource.resource_uri()
    return response

def resource_response(resource, current_request):
    result_dict = resource.as_dict()
    if _get_mimetype(current_request) == JSON:
        return _single_resource_json_response(resource)
    else:
        return _single_resource_html_response(resource)


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

def update_resource(resource, data):
    """Replace the contents of a resource with *data* and return an appropriate
    *Response*.
    
    :param resource: :class:`sandman.model.Resource` to be updated
    :param data: New values for the fields in *resource*

    """

    resource.from_dict(request.json)
    session = _get_session()
    session.merge(resource)
    session.commit()
    return no_content_response()


@app.route('/<collection>/<key>', methods=['PATCH'])
def patch_resource(collection, key):
    """"Upsert" a resource identified by the given key and return the appropriate
    *Response*.
    
    If no resource currently exists at `/<collection>/<key>`, create it
    with *key* as its primary key and return a
    :func:`resource_created_response`.

    If a resource *does* exist at `/<collection>/<key>`, update it with
    the data sent in the request and return a :func:`no_content_response`.

    Note: HTTP `PATCH` (and, thus, :func:`patch_resource`) is idempotent

    :param string collection: a :class:`sandman.model.Resource` endpoint
    :param string key: the primary key for the associated :class:`sandman.model.Resource`
    :rtype: :class:`flask.Response`

    """
    session = _get_session()
    with app.app_context():
        cls = current_app.endpoint_classes[collection]

    resource = session.query(cls).get(key)

    if not _validate(cls, request.method, resource):
        return unsupported_method_response()

    if resource is None:
        resource = cls()
        resource.from_dict(request.json)
        setattr(resource, resource.primary_key(), key)
        session.add(resource)
        session.commit()
        return resource_created_response(resource, request)
    else:
        return update_resource(resource, request.json)

@app.route('/<collection>/<key>', methods=['PUT'])
def replace_resource(collection, key):
    """Replace the resource identified by the given key and return the appropriate
    response.

    :param string collection: a :class:`sandman.model.Resource` endpoint
    :rtype: :class:`flask.Response`

    """
    resource = retrieve_resource(collection, key)

    if resource is None:
        return JSONException('Requested resource not found', code=404)
    elif not _validate(endpoint_class(collection), request.method, resource):
        return unsupported_method_response()

    resource.replace(request.json)
    session = _get_session()
    session.add(resource)
    try:
        session.commit()
    except IntegrityError as e:
        return JSONException('Requested resource not found. Exception: [{}]'.format(e.message), code=422)
    return no_content_response()

@app.route('/<collection>', methods=['POST'])
def add_resource(collection):
    """Return the appropriate *Response* based on adding a new resource to *collection*

    :param string collection: a :class:`sandman.model.Resource` endpoint
    :rtype: :class:`flask.Response`

    """
    cls = endpoint_class(collection)
    resource = cls()
    resource.from_dict(request.json)

    if not _validate(cls, request.method, resource):
        return unsupported_method_response()

    session = _get_session()
    session.add(resource)
    session.commit()
    return resource_created_response(resource, request)

@app.route('/<collection>/<key>', methods=['DELETE'])
def delete_resource(collection, key):
    """Return the appropriate *Response* for deleting an existing resource in *collection*
    
    :param string collection: a :class:`sandman.model.Resource` endpoint
    :param string key: the primary key for the associated :class:`sandman.model.Resource`
    :rtype: :class:`flask.Response`

    """
    with app.app_context():
        cls = current_app.endpoint_classes[collection]
    resource = cls()
    session = _get_session()
    resource = session.query(cls).get(key)

    if resource is None:
        return JSONException('Requested resource not found', code=404)
    elif not _validate(endpoint_class(collection), request.method, resource):
        return unsupported_method_response()

    session.delete(resource)
    session.commit()
    return no_content_response()


@app.route('/<collection>/<key>', methods=['GET'])
def show_resource(collection, key):
    """Return the appropriate *Response* for retrieving a single resource
    
    :param string collection: a :class:`sandman.model.Resource` endpoint
    :param string key: the primary key for the associated :class:`sandman.model.Resource`
    :rtype: :class:`flask.Response`

    """
    resource = retrieve_resource(collection, key)
    
    if resource is None:
        return JSONException('Requested resource not found', code=404)
    elif not _validate(endpoint_class(collection), request.method, resource):
        return unsupported_method_response()

    return resource_response(resource, request)

@app.route('/<collection>', methods=['GET'])
def show_collection(collection):
    """Return the appropriate *Response* for retrieving a collection of resources
    
    :param string collection: a :class:`sandman.model.Resource` endpoint
    :param string key: the primary key for the associated :class:`sandman.model.Resource`
    :rtype: :class:`flask.Response`

    """
    with app.app_context():
        cls = current_app.endpoint_classes[collection]
    session = _get_session()
    resources = session.query(cls).all()

    if not _validate(endpoint_class(collection), request.method, resources):
        return unsupported_method_response()

    if _get_mimetype(request) == JSON:
        return _collection_json_response(resources)
    else:
        return _collection_html_response(resources)
