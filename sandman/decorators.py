import functools
import hashlib
from flask import jsonify, request, url_for, current_app, make_response, g

def cache_control(*directives):
    def decorator(f):
        @functools.wraps(f)
        def wrapped(*args, **kwargs):
            rv = f(*args, **kwargs)
            rv = make_response(rv)
            rv.headers['Cache-Control'] =', '.join(directives)
            return rv
        return wrapped
    return decorator


def no_cache(f):
    return cache_control('no-cache', 'no-store', 'max-age=0')(f)


def etag(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        # only for HEAD and GET requests
        assert request.method in ['HEAD', 'GET'],\
            '@etag is only supported for GET requests'
        rv = f(*args, **kwargs)
        rv = make_response(rv)
        etag = '"' + hashlib.md5(rv.get_data()).hexdigest() + '"'
        rv.headers['ETag'] = etag
        if_match = request.headers.get('If-Match')
        if_none_match = request.headers.get('If-None-Match')
        if if_match:
            etag_list = [tag.strip() for tag in if_match.split(',')]
            if etag not in etag_list and '*' not in etag_list:
                rv = precondition_failed()
        elif if_none_match:
            etag_list = [tag.strip() for tag in if_none_match.split(',')]
            if etag in etag_list or '*' in etag_list:
                rv = not_modified()
        return rv
    return wrapped


def not_modified():
    response = jsonify({'status': 304, 'error': 'not modified'})
    response.status_code = 304
    return response


def precondition_failed():
    response = jsonify({'status': 412, 'error': 'precondition failed'})
    response.status_code = 412
    return response
