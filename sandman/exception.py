"""Exception specifications for Sandman"""

from werkzeug.exceptions import HTTPException

class JSONException(HTTPException):
    def __init__(self, description=None, code=400, response=None):
        super(JSONException, self).__init__(description, response)
        self.code = code

    def get_headers():
        return [{'Content-type': 'application/json'}]

    def get_body():
        return jsonify({'result': False, 'message': self.message})
