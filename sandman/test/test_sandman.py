"""Main test class for sandman"""

from sandman import app, db
import unittest

class SandmanTestCase(unittest.TestCase):

    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/jknupp/code/github_code/sandman/sandman/test/chinook'
        app.config['TESTING'] = True
        self.app = app.test_client()
        import models

    def tearDown(self):
        pass

    def test_get_artists(self):
        import json
        response = self.app.get('/artists')
        assert response.status_code == 200
        assert response.data
        assert len(json.loads(response.data)['resources']) == 275
