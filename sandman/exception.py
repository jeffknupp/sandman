"""Exception specifications for Sandman"""

from werkzeug.exceptions import HTTPException
from flask import jsonify

class JSONException(HTTPException):
    """Excecption which generates a :class:`flask.Response` object whose
    *data* is JSON rather than HTML"""

    def __init__(self, description=None, code=400, response=None):
        super(JSONException, self).__init__(description, response)
        self.code = code

    def get_headers(self, environ=None):
        """Return the appropriate content-type: *application/json*"""
        return[('Content-type', 'application/json')]

    def get_body(self, environ=None):
        """Return the body of the *reponse* serialized as JSON"""
        return jsonify({'result': False, 'message': self.message})
