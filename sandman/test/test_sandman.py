"""Main test class for sandman"""

from sandman import app, db
import unittest
import os
import shutil
import json

class SandmanTestCase(unittest.TestCase):

    DB_LOCATION = os.path.join(os.getcwd(), 'sandman', 'test', 'chinook')
    def setUp(self):
        
        shutil.copy(os.path.join(os.getcwd(), 'sandman', 'test', 'data', 'chinook'), self.DB_LOCATION) 
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + self.DB_LOCATION
        app.config['TESTING'] = True
        self.app = app.test_client()
        from . import models

    def tearDown(self):
        os.unlink(self.DB_LOCATION)
        self.app = None

    def test_get(self):
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
        assert response.status_code == 201
        assert type(response.data) == str
        assert json.loads(response.data)['Name'] == u'Jeff Knupp'
        self.assertEqual(json.loads(response.data)['links'], [{u'rel': u'self', u'uri': u'/artists/276'}])

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

    def test_delete_non_existant_resource(self):
        response = self.app.delete('/artists/404')
        assert response.status_code == 404

    def test_delete_not_supported(self):
        response = self.app.delete('/playlists/1')
        assert response.status_code == 403

    def test_get_user_defined_methods(self):
        response = self.app.post('/styles',
                content_type='application/json', 
                data=json.dumps({u'Name': u'Hip-Hop'}))
        assert response.status_code == 403
        assert not response.data 

    def test_get_unsupported_resource_method(self):
        response = self.app.patch('/styles/26',
                content_type='application/json', 
                data=json.dumps({u'Name': u'Hip-Hop'}))
        assert response.status_code == 403

    def test_get_supported_method(self):
        response = self.app.get('/styles/5')
        assert response.status_code == 200


    def test_get_unsupported_collection_method(self):
        response = self.app.get('/albums')
        assert response.status_code == 403


    def test_get_user_defined_endpoint(self):
        response = self.app.get('/styles')
        assert response.status_code == 200
        assert response.data
        assert len(json.loads(response.data)[u'resources']) == 25

    def test_user_validation(self):
        response = self.app.get('/styles/1')
        assert response.status_code == 403

    def test_get_html(self):
        response = self.app.get('/artists/1', headers={'Accept': 'text/html'})
        assert response.status_code == 200
        assert '<!DOCTYPE html>' in response.data

    def test_get_html_collection(self):
        response = self.app.get('/artists', headers={'Accept': 'text/html'})
        assert response.status_code == 200
        assert '<!DOCTYPE html>' in response.data
        assert 'Aerosmith' in response.data

    def test_explicit_get_json(self):
        response = self.app.get('/artists', headers={'Accept': 'application/json'})
        assert response.status_code == 200
        assert response.data
        assert len(json.loads(response.data)[u'resources']) == 275

    def test_post_html_response(self):
        response = self.app.post('/artists', 
                content_type='application/json', 
                headers={'Accept': 'text/html'},
                data=json.dumps({u'Name': u'Jeff Knupp'}))
        assert response.status_code == 201
        assert 'Jeff Knupp' in response.data
