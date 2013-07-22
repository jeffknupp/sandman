"""Exception specifications for Sandman"""

from werkzeug.exceptions import HTTPException
from flask import jsonify

class JSONException(HTTPException):
    """Excecption returned with JSON data rather than HTML"""
    def __init__(self, description=None, code=400, response=None):
        super(JSONException, self).__init__(description, response)
        self.code = code

    def get_headers(self, environ=None):
        return [{'Content-type': 'application/json'}]

    def get_body(self, environ=None):
        return jsonify({'result': False, 'message': self.message})
