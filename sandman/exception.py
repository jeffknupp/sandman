"""Exception specifications for Sandman"""

from werkzeug.exceptions import HTTPException
from flask import jsonify, abort, make_response, render_template

class InvalidAPIUsage(Exception):
    """Excecption which generates a :class:`flask.Response` object whose
    *data* is JSON rather than HTML"""

    def __init__(self, code=400, message=None, payload=None):
        super(Exception, self).__init__(message)
        self.message = message
        self.payload = payload
        if code is not None:
            self.code = code

    def to_dict(self):
        as_dict = dict(self.payload or ())
        as_dict['message'] = self.message
        return as_dict

    def abort(self):
        resp = make_response(render_template('error.html', error=self.code, message=self.message), self.code)
        return resp
