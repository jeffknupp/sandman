"""Sandman REST API creator for Flask and SQLAlchemy"""

from flask import (jsonify, request, g,
        current_app, Response, render_template,
        make_response)
from sqlalchemy.exc import IntegrityError
from . import app, db
from .exception import InvalidAPIUsage
from .model.models import Model
from .model.utils import _get_session

JSON, HTML = range(2)
JSON_CONTENT_TYPES = set(['application/json',])
HTML_CONTENT_TYPES = set(['text/html', 'application/x-www-form-urlencoded'])
ALL_CONTENT_TYPES = set(['*/*'])
ACCEPTABLE_CONTENT_TYPES = (JSON_CONTENT_TYPES | HTML_CONTENT_TYPES
        | ALL_CONTENT_TYPES)

FORWARDED_EXCEPTION_MESSAGE = 'Request could not be completed. Exception: [{}]'
FORBIDDEN_EXCEPTION_MESSAGE = """Method [{}] not acceptable for resource \
type [{}].  Acceptable methods: [{}]"""
UNSUPPORTED_CONTENT_TYPE_MESSAGE = """Content-type [{}] not supported.
Supported values for 'Content-type': {}""".format(
        '{}', str(ACCEPTABLE_CONTENT_TYPES))

def _perform_database_action(action, *args):
    """Call session.*action* with the given *args*.

    Will later be used to abstract away database backend.
    """
    session = _get_session()
    getattr(session, action)(*args)
    session.commit()

def _get_acceptable_response_type():
    """Return the mimetype for this request."""
    if ('Accept' not in request.headers or request.headers['Accept'] in
            ALL_CONTENT_TYPES):
        return JSON
    acceptable_content_types = set(request.headers['ACCEPT'].strip().split(','))
    if acceptable_content_types & HTML_CONTENT_TYPES:
        return HTML
    elif acceptable_content_types & JSON_CONTENT_TYPES:
        return JSON
    else:
        # HTTP 406 Not Acceptable
        raise InvalidAPIUsage(406)

@app.errorhandler(InvalidAPIUsage)
def handle_exception(error):
    """Return a response with the appropriate status code, message, and content
    type when an ``InvalidAPIUsage`` exception is raised."""
    try:
        if _get_acceptable_response_type() == JSON:
            response = jsonify(error.to_dict())
            response.status_code = error.code
            return response
        else:
            return error.abort()
    except InvalidAPIUsage as _:
        # In addition to the original exception, we don't support the content
        # type in the request's 'Accept' header, which is a more important
        # error, so return that instead of what was originally raised.
        response = jsonify(error.to_dict())
        response.status_code = 415
        return response

def _single_attribute_json_response(name, value):
    """Return the json representation of a single attribute of a resource.

    :param string name:  name of the attribute
    :param string value: string value of the attribute
    :rtype: :class:`flask.Response`

    """
    return jsonify({name: str(value)})

def _single_resource_json_response(resource):
    """Return the JSON representation of *resource*.

    :param resource: :class:`sandman.model.Model` to render
    :type resource: :class:`sandman.model.Model`
    :rtype: :class:`flask.Response`

    """
    return jsonify(**resource.as_dict())

def _single_attribute_html_response(resource, name, value):
    """Return the json representation of a single attribute of a resource.

    :param :class:`sandman.model.Model` resource: resource to get attribute from
    :param string name:  name of the attribute
    :param string value: string value of the attribute
    :rtype: :class:`flask.Response`

    """
    return make_response(render_template('attribute.html', resource=resource,
        name=name, value=value))

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

def _collection_html_response(resources, start=0, stop=20):
    """Return the HTML representation of the collection *resources*.

    :param list resources: list of :class:`sandman.model.Model`s to render
    :rtype: :class:`flask.Response`

    """
    return make_response(render_template('collection.html',
        resources=resources[start:stop]))

def _validate(cls, method, resource=None):
    """Return ``True`` if the the given *cls* supports the HTTP *method* found
    on the incoming HTTP request.

    :param cls: class associated with the request's endpoint
    :type cls: :class:`sandman.model.Model` instance
    :param string method: HTTP method of incoming request
    :param resource: *cls* instance associated with the request
    :type resource: :class:`sandman.model.Model` or list of
                    :class:`sandman.model.Model` or None
    :rtype: bool

    """
    if method not in cls.__methods__:
        raise InvalidAPIUsage(403, FORBIDDEN_EXCEPTION_MESSAGE.format(method,
            cls.endpoint(), cls.__methods__))

    class_validator_name = 'validate_' + method

    if hasattr(cls, class_validator_name):
        class_validator = getattr(cls, class_validator_name)
        if not class_validator(resource):
            raise InvalidAPIUsage(403)

def get_resource_data(incoming_request):
    """Return the data from the incoming *request* based on the Content-type."""
    content_type = incoming_request.headers['Content-type'].split(';')[0]
    if ('Content-type' not in incoming_request.headers or
            content_type in JSON_CONTENT_TYPES):
        return incoming_request.json
    elif content_type in HTML_CONTENT_TYPES:
        if not incoming_request.form:
            raise InvalidAPIUsage(400)
        return incoming_request.form
    else:
        # HTTP 415: Unsupported Media Type
        raise InvalidAPIUsage(415,
                UNSUPPORTED_CONTENT_TYPE_MESSAGE.format(
                    incoming_request.headers['Content-type']))

def endpoint_class(collection):
    """Return the :class:`sandman.model.Model` associated with the endpoint
    *collection*.

    :param string collection: a :class:`sandman.model.Model` endpoint
    :rtype: :class:`sandman.model.Model`

    """
    with app.app_context():
        try:
            cls = current_app.class_references[collection]
        except KeyError:
            raise InvalidAPIUsage(404)
        return cls

def retrieve_collection(collection, query_arguments=None):
    """Return the resources in *collection*, possibly filtered by a series of
    values to use in a 'where' clause search.

    :param string collection: a :class:`sandman.model.Model` endpoint
    :param dict query_arguments: a list of filter query arguments
    :rtype: class:`sandman.model.Model`

    """
    session = _get_session()
    cls = endpoint_class(collection)
    if query_arguments:
        filters = []
        order = []
        for key, value in query_arguments.items():
            if key == 'page':
                continue
            if value.startswith('%'):
                filters.append(getattr(cls, key).like(str(value), escape='/'))
            elif key == 'sort':
                order.append(getattr(cls, value))
            elif key:
                filters.append(getattr(cls, key) == value)
        resources = session.query(cls).filter(*filters).order_by(*order)
    else:
        resources = session.query(cls).all()
    return resources


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
    if _get_acceptable_response_type() == JSON:
        response = _single_resource_json_response(resource)
    else:
        response = _single_resource_html_response(resource)
    response.status_code = 201
    response.headers['Location'] = 'http://localhost:5000/{}'.format(
            resource.resource_uri())
    return response

def collection_response(resources, start=None, stop=None):
    """Return a response for the *resources* of the appropriate content type.

    :param resources: resources to be returned in request
    :type resource: list of :class:`sandman.model.Model`
    :rtype: :class:`flask.Response`

    """
    if _get_acceptable_response_type() == JSON:
        return _collection_json_response(resources)
    else:
        return _collection_html_response(resources, start, stop)


def resource_response(resource):
    """Return a response for the *resource* of the appropriate content type.

    :param resource: resource to be returned in request
    :type resource: :class:`sandman.model.Model`
    :rtype: :class:`flask.Response`

    """
    if _get_acceptable_response_type() == JSON:
        return _single_resource_json_response(resource)
    else:
        return _single_resource_html_response(resource)

def attribute_response(resource, name, value):
    """Return a response for the *resource* of the appropriate content type.

    :param resource: resource to be returned in request
    :type resource: :class:`sandman.model.Model`
    :rtype: :class:`flask.Response`

    """
    if _get_acceptable_response_type() == JSON:
        return _single_attribute_json_response(name, value)
    else:
        return _single_attribute_html_response(resource, name, value)


def no_content_response():
    """Return the appropriate *Response* with status code *204*, signaling a
    completed action which does not require data in the response body

    :rtype: :class:`flask.Response`

    """
    response = Response()
    response.status_code = 204
    return response

def update_resource(resource, incoming_request):
    """Replace the contents of a resource with *data* and return an appropriate
    *Response*.

    :param resource: :class:`sandman.model.Model` to be updated
    :param data: New values for the fields in *resource*

    """
    resource.from_dict(get_resource_data(incoming_request))
    _perform_database_action('merge', resource)
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
    cls = endpoint_class(collection)

    try:
        resource = retrieve_resource(collection, key)
    except InvalidAPIUsage:
        resource = None

    _validate(cls, request.method, resource)

    if resource is None:
        resource = cls()
        resource.from_dict(get_resource_data(request))
        setattr(resource, resource.primary_key(), key)
        _perform_database_action('add', resource)
        return resource_created_response(resource)
    else:
        return update_resource(resource, request)

@app.route('/<collection>/<key>', methods=['PUT'])
def put_resource(collection, key):
    """Replace the resource identified by the given key and return the
    appropriate response.

    :param string collection: a :class:`sandman.model.Model` endpoint
    :rtype: :class:`flask.Response`

    """
    resource = retrieve_resource(collection, key)

    _validate(endpoint_class(collection), request.method, resource)

    resource.replace(get_resource_data(request))
    try:
        _perform_database_action('add', resource)
    except IntegrityError as exception:
        raise InvalidAPIUsage(422, FORWARDED_EXCEPTION_MESSAGE.format(
            exception.message))
    return no_content_response()

@app.route('/<collection>', methods=['POST'])
def post_resource(collection):
    """Return the appropriate *Response* based on adding a new resource to
    *collection*.

    :param string collection: a :class:`sandman.model.Model` endpoint
    :rtype: :class:`flask.Response`

    """
    cls = endpoint_class(collection)
    resource = cls()
    resource.from_dict(get_resource_data(request))

    _validate(cls, request.method, resource)

    _perform_database_action('add', resource)
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
    resource = retrieve_resource(collection, key)

    _validate(cls, request.method, resource)

    try:
        _perform_database_action('delete', resource)
    except IntegrityError as exception:
        raise InvalidAPIUsage(422, FORWARDED_EXCEPTION_MESSAGE.format(
            exception.message))
    return no_content_response()

@app.route('/<collection>/<key>', methods=['GET'])
def get_resource(collection, key):
    """Return the appropriate *Response* for retrieving a single resource.

    :param string collection: a :class:`sandman.model.Model` endpoint
    :param string key: the primary key for the :class:`sandman.model.Model`
    :rtype: :class:`flask.Response`

    """
    resource = retrieve_resource(collection, key)
    _validate(endpoint_class(collection), request.method, resource)

    return resource_response(resource)

@app.route('/<collection>/<key>/<attribute>', methods=['GET'])
def get_resource_attribute(collection, key, attribute):
    """Return the appropriate *Response* for retrieving an attribute of
    a single resource.

    :param string collection: a :class:`sandman.model.Model` endpoint
    :param string key: the primary key for the :class:`sandman.model.Model`
    :rtype: :class:`flask.Response`

    """
    resource = retrieve_resource(collection, key)
    _validate(endpoint_class(collection), request.method, resource)
    value = getattr(resource, attribute)
    if isinstance(value, Model):
        return resource_response(value)
    else:
        return attribute_response(resource, attribute, value)


@app.route('/<collection>', methods=['GET'])
def get_collection(collection):
    """Return the appropriate *Response* for retrieving a collection of
    resources.

    :param string collection: a :class:`sandman.model.Model` endpoint
    :param string key: the primary key for the :class:`sandman.model.Model`
    :rtype: :class:`flask.Response`

    """
    cls = endpoint_class(collection)

    resources = retrieve_collection(collection, request.args)

    _validate(cls, request.method, resources)

    start, stop = 1, 20

    if request.args and 'page' in request.args:
        page = int(request.args['page'])
        results_per_page = app.config.get('RESULTS_PER_PAGE', 20)
        start, stop = page * results_per_page, (page * results_per_page) + 1
    return collection_response(resources, start, stop)
