"""Main test class for sandman"""

from sandman import app, db
import unittest
import os
import shutil
import json

class SandmanTestCase(unittest.TestCase):

    DB_LOCATION = os.path.join(os.getcwd(), 'sandman', 'test', 'chinook')
    def setUp(self):
        
        if os.path.exists(self.DB_LOCATION):
            os.unlink(self.DB_LOCATION)
        shutil.copy(os.path.join(os.getcwd(), 'sandman', 'test', 'data', 'chinook'), self.DB_LOCATION) 
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + self.DB_LOCATION
        app.config['TESTING'] = True
        self.app = app.test_client()
        from . import models

    def tearDown(self):
        os.unlink(self.DB_LOCATION)
        self.app = None

    def test_get(self):
        import json
        response = self.app.get('/artists')
        assert response.status_code == 200
        assert response.data
        assert len(json.loads(response.data)[u'resources']) == 275

    def test_post(self):
        response = self.app.post('/artists', 
                content_type='application/json', 
                data=json.dumps({u'Name': u'Jeff Knupp'}))
        assert response.status_code == 201
        assert json.loads(response.data)[u'Name'] == u'Jeff Knupp'
        self.assertEqual(json.loads(response.data)[u'links'], [{u'rel': u'self', u'uri': u'/artists/276'}])

    def test_get_posted_resource(self):
        post_response = self.app.post('/artists', 
                content_type='application/json', 
                data=json.dumps({u'Name': u'Jeff Knupp'}))
        location = post_response.headers['Location']
        as_json = json.loads(post_response.data)
        uri = as_json[u'links'][0][u'uri']
        response = self.app.get(location)
        assert response.status_code == 200
        response = self.app.get(uri)
        assert response.status_code == 200
        assert as_json[u'Name'] == u'Jeff Knupp'

    def test_patch_new_resource(self):
        response = self.app.patch('/artists/276', 
                content_type='application/json', 
                data=json.dumps({u'Name': u'Jeff Knupp'}))
        #assert response.status_code == 201
        assert type(response.data) == str
        #assert json.loads(response.data) == u'Jeff Knupp'
        #self.assertEqual(json.loads(response.data)['links'], [{u'rel': u'self', u'uri': u'/artists/276'}])

    def test_patch_existing_resource(self):
        response = self.app.patch('/artists/275', 
                content_type='application/json', 
                data=json.dumps({u'Name': u'Jeff Knupp'}))
        assert response.status_code == 204
        response = self.app.get(u'/artists/275')
        assert response.status_code == 200
        assert json.loads(response.data.decode('utf-8'))[u'Name'] == u'Jeff Knupp'
        assert json.loads(response.data.decode('utf-8'))[u'ArtistId'] == 275

    def test_delete_resource(self):
        response = self.app.delete('/artists/275')
        assert response.status_code == 204
        response = self.app.get('/artists/275')
        assert response.status_code == 404
