import functools
import hashlib
from flask import jsonify, request, url_for, current_app, make_response, g
from .rate_limit import RateLimit
from .errors import too_many_requests, precondition_failed, not_modified


def json(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        rv = f(*args, **kwargs)
        status_or_headers = None
        headers = None
        if isinstance(rv, tuple):
            rv, status_or_headers, headers = rv + (None,) * (3 - len(rv))
        if isinstance(status_or_headers, (dict, list)):
            headers, status_or_headers = status_or_headers, None
        if not isinstance(rv, dict):
            rv = rv.to_json()
        rv = jsonify(rv)
        if status_or_headers is not None:
            rv.status_code = status_or_headers
        if headers is not None:
            rv.headers.extend(headers)
        return rv
    return wrapped


def rate_limit(limit, per, scope_func=lambda: request.remote_addr):
    def decorator(f):
        @functools.wraps(f)
        def wrapped(*args, **kwargs):
            if current_app.config['USE_RATE_LIMITS']:
                key = 'rate-limit/%s/%s/' % (f.__name__, scope_func())
                limiter = RateLimit(key, limit, per)
                if not limiter.over_limit:
                    rv = f(*args, **kwargs)
                else:
                    rv = too_many_requests('You have exceeded your request rate')
                #rv = make_response(rv)
                g.headers = {
                    'X-RateLimit-Remaining': str(limiter.remaining),
                    'X-RateLimit-Limit': str(limiter.limit),
                    'X-RateLimit-Reset': str(limiter.reset)
                }
                return rv
            else:
                return f(*args, **kwargs)
        return wrapped
    return decorator


def paginate(max_per_page=10):
    def decorator(f):
        @functools.wraps(f)
        def wrapped(*args, **kwargs):
            page = request.args.get('page', 1, type=int)
            per_page = min(request.args.get('per_page', max_per_page,
                                            type=int), max_per_page)
            query = f(*args, **kwargs)
            p = query.paginate(page, per_page)
            pages = {'page': page, 'per_page': per_page,
                     'total': p.total, 'pages': p.pages}
            if p.has_prev:
                pages['prev'] = url_for(request.endpoint, page=p.prev_num,
                                        per_page=per_page,
                                        _external=True, **kwargs)
            else:
                pages['prev'] = None
            if p.has_next:
                pages['next'] = url_for(request.endpoint, page=p.next_num,
                                        per_page=per_page,
                                        _external=True, **kwargs)
            else:
                pages['next'] = None
            pages['first'] = url_for(request.endpoint, page=1,
                                     per_page=per_page, _external=True,
                                     **kwargs)
            pages['last'] = url_for(request.endpoint, page=p.pages,
                                    per_page=per_page, _external=True,
                                    **kwargs)
            return jsonify({
                'urls': [item.get_url() for item in p.items],
                'meta': pages
            })
        return wrapped
    return decorator


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
