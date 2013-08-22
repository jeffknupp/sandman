"""Sandman REST API creator for Flask and SQLAlchemy"""

from flask import (jsonify, request, g,
        current_app, Response, render_template,
        make_response)
from sqlalchemy.exc import IntegrityError
from . import app, db
from .exception import InvalidAPIUsage

JSON, HTML = range(2)

FORWARDED_EXCEPTION_MESSAGE = 'Requested resource not found. Exception: [{}]'

def _get_session():
    """Return (and memoize) a database session"""
    session = getattr(g, '_session', None)
    if session is None:
        session = g._session = db.session()
    return session

def _get_mimetype():
    """Return the mimetype for this request."""
    if 'Accept' not in request.headers:
        return JSON

    if 'html' in request.headers['Accept']:
        return HTML
    else:
        return JSON

@app.errorhandler(InvalidAPIUsage)
def handle_exception(error):
    if _get_mimetype() == JSON:
        response = jsonify(error.to_dict())
        response.status_code = error.code
        return response
    else:
        return error.abort()


def _single_resource_json_response(resource):
    """Return the JSON representation of *resource*.

    :param resource: :class:`sandman.model.Model` to render
    :type resource: :class:`sandman.model.Model`
    :rtype: :class:`flask.Response`

    """
    return jsonify(**resource.as_dict())

def _single_resource_html_response(resource):
    """Return the HTML representation of *resource*.

    :param resource: :class:`sandman.model.Model` to render
    :type resource: :class:`sandman.model.Model`
    :rtype: :class:`flask.Response`

    """
    tablename = resource.__tablename__
    resource.pk = getattr(resource, resource.primary_key())
    resource.attributes = resource.as_dict()
    return make_response(render_template('resource.html', resource=resource,
        tablename=tablename))

def _collection_json_response(resources):
    """Return the JSON representation of the collection *resources*.

    :param list resources: list of :class:`sandman.model.Model`s to render
    :rtype: :class:`flask.Response`

    """
    result_list = []
    for resource in resources:
        result_list.append(resource.as_dict())
    return jsonify(resources=result_list)

def _collection_html_response(resources):
    """Return the HTML representation of the collection *resources*.

    :param list resources: list of :class:`sandman.model.Model`s to render
    :rtype: :class:`flask.Response`

    """
    return make_response(render_template('collection.html',
        resources=resources))

def _validate(cls, method, resource=None):
    """Return ``True`` if the the given *cls* supports the HTTP *method* found
    on the incoming HTTP request.

    :param cls: class associated with the request's endpoint
    :type cls: :class:`sandman.model.Model` instance
    :param string method: HTTP method of incoming request
    :param resource: *cls* instance associated with the request
    :type resource: :class:`sandman.model.Model` or None
    :rtype: bool

    """
    if not cls or not method in cls.__methods__:
        raise InvalidAPIUsage(403)

    class_validator_name = 'validate_' + method

    if hasattr(cls, class_validator_name):
        class_validator = getattr(cls, class_validator_name)
        if not class_validator(resource):
            raise InvalidAPIUsage(403)

def endpoint_class(collection):
    """Return the :class:`sandman.model.Model` associated with the endpoint
    *collection*.

    :param string collection: a :class:`sandman.model.Model` endpoint
    :rtype: :class:`sandman.model.Model`

    """
    with app.app_context():
        try:
            cls = current_app.endpoint_classes[collection]
        except KeyError:
            raise InvalidAPIUsage(404)
        return cls

def retrieve_resource(collection, key):
    """Return the resource in *collection* identified by key *key*.

    :param string collection: a :class:`sandman.model.Model` endpoint
    :param string key: primary key of resource
    :rtype: class:`sandman.model.Model`

    """
    session = _get_session()
    cls = endpoint_class(collection)
    resource = session.query(cls).get(key)
    if resource is None:
        raise InvalidAPIUsage(404)
    return resource

def resource_created_response(resource):
    """Return HTTP response with status code *201*, signaling a created
    *resource*

    :param resource: resource created as a result of current request
    :type resource: :class:`sandman.model.Model`
    :rtype: :class:`flask.Response`

    """
    if _get_mimetype() == JSON:
        response = _single_resource_json_response(resource)
    else:
        response = _single_resource_html_response(resource)
    response.status_code = 201
    response.headers['Location']  = 'http://localhost:5000/{}'.format(
            resource.resource_uri())
    return response

def resource_response(resource, current_request):
    """Return a response for the *resource* given the mimetype header value in
    the *current_request*.

    :param resource: resource created as a result of current request
    :type resource: :class:`sandman.model.Model`
    :param current_request: :class:`flask.Request` request being handled
    :type current_request: :class:`flask.Request`
    :rtype: :class:`flask.Response`

    """
    if _get_mimetype() == JSON:
        return _single_resource_json_response(resource)
    else:
        return _single_resource_html_response(resource)

def no_content_response():
    """Return the appropriate *Response* with status code *204*, signaling a
    completed action which does not require data in the response body

    :rtype: :class:`flask.Response`

    """
    response = Response()
    response.status_code = 204
    return response

def update_resource(resource, data):
    """Replace the contents of a resource with *data* and return an appropriate
    *Response*.

    :param resource: :class:`sandman.model.Model` to be updated
    :param data: New values for the fields in *resource*

    """
    resource.from_dict(data)
    session = _get_session()
    session.merge(resource)
    session.commit()
    return no_content_response()


@app.route('/<collection>/<key>', methods=['PATCH'])
def patch_resource(collection, key):
    """"Upsert" a resource identified by the given key and return the
    appropriate *Response*.

    If no resource currently exists at `/<collection>/<key>`, create it
    with *key* as its primary key and return a
    :func:`resource_created_response`.

    If a resource *does* exist at `/<collection>/<key>`, update it with
    the data sent in the request and return a :func:`no_content_response`.

    Note: HTTP `PATCH` (and, thus, :func:`patch_resource`) is idempotent

    :param string collection: a :class:`sandman.model.Model` endpoint
    :param string key: the primary key for the :class:`sandman.model.Model`
    :rtype: :class:`flask.Response`

    """
    session = _get_session()
    cls = endpoint_class(collection)

    try:
        resource = retrieve_resource(collection, key)
    except InvalidAPIUsage:
        resource = None

    _validate(cls, request.method, resource)

    if resource is None:
        resource = cls()
        resource.from_dict(request.json)
        setattr(resource, resource.primary_key(), key)
        session.add(resource)
        session.commit()
        return resource_created_response(resource)
    else:
        return update_resource(resource, request.json)

@app.route('/<collection>/<key>', methods=['PUT'])
def replace_resource(collection, key):
    """Replace the resource identified by the given key and return the
    appropriate response.

    :param string collection: a :class:`sandman.model.Model` endpoint
    :rtype: :class:`flask.Response`

    """
    resource = retrieve_resource(collection, key)

    if resource is None:
        raise InvalidAPIUsage(404, 'Requested resource not found')

    _validate(endpoint_class(collection), request.method, resource)

    resource.replace(request.json)
    session = _get_session()
    session.add(resource)
    try:
        session.commit()
    except IntegrityError as exception:
        raise InvalidAPIUsage(422, FORWARDED_EXCEPTION_MESSAGE.format(exception.message))
    return no_content_response()

@app.route('/<collection>', methods=['POST'])
def add_resource(collection):
    """Return the appropriate *Response* based on adding a new resource to
    *collection*.

    :param string collection: a :class:`sandman.model.Model` endpoint
    :rtype: :class:`flask.Response`

    """
    cls = endpoint_class(collection)
    if cls is None:
        raise InvalidAPIUsage(404)
    resource = cls()
    resource.from_dict(request.json)

    _validate(cls, request.method, resource)

    session = _get_session()
    session.add(resource)
    session.commit()
    return resource_created_response(resource)

@app.route('/<collection>/<key>', methods=['DELETE'])
def delete_resource(collection, key):
    """Return the appropriate *Response* for deleting an existing resource in
    *collection*.

    :param string collection: a :class:`sandman.model.Model` endpoint
    :param string key: the primary key for the :class:`sandman.model.Model`
    :rtype: :class:`flask.Response`

    """
    cls = endpoint_class(collection)
    resource = cls()
    session = _get_session()
    resource = retrieve_resource(collection, key)

    if resource is None:
        raise InvalidAPIUsage(404, 'Requested resource not found')

    _validate(cls, request.method, resource)

    try:
        session.delete(resource)
        session.commit()
    except IntegrityError as exception:
        raise InvalidAPIUsage(422, FORWARDED_EXCEPTION_MESSAGE.format(exception.message))
    return no_content_response()


@app.route('/<collection>/<key>', methods=['GET'])
def show_resource(collection, key):
    """Return the appropriate *Response* for retrieving a single resource

    :param string collection: a :class:`sandman.model.Model` endpoint
    :param string key: the primary key for the :class:`sandman.model.Model`
    :rtype: :class:`flask.Response`

    """
    resource = retrieve_resource(collection, key)

    if resource is None:
        raise InvalidAPIUsage(404, 'Requested resource not found')

    _validate(endpoint_class(collection), request.method, resource)

    return resource_response(resource, request)

@app.route('/<collection>', methods=['GET'])
def show_collection(collection):
    """Return the appropriate *Response* for retrieving a collection of
    resources.

    :param string collection: a :class:`sandman.model.Model` endpoint
    :param string key: the primary key for the :class:`sandman.model.Model`
    :rtype: :class:`flask.Response`

    """
    cls = endpoint_class(collection)
    session = _get_session()
    resources = session.query(cls).all()

    _validate(cls, request.method, resources)

    if _get_mimetype() == JSON:
        return _collection_json_response(resources)
    else:
        return _collection_html_response(resources)
