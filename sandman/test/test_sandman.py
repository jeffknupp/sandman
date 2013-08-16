"""Main test class for sandman"""

from sandman import app
import os
import shutil
import json

class TestSandman(object):
    DB_LOCATION = os.path.join(os.getcwd(), 'sandman', 'test', 'chinook')

    def setup_method(self, _):
        """Grab the database file from the *data* directory and configure the
        app."""
        shutil.copy(
                os.path.join(
                    os.getcwd(),
                    'sandman',
                    'test',
                    'data',
                    'chinook'),
                self.DB_LOCATION)
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + self.DB_LOCATION
        app.config['TESTING'] = True
        self.app = app.test_client()
        from . import models

    def teardown_method(self, _):
        """Remove the database file copied during setup."""
        os.unlink(self.DB_LOCATION)
        self.app = None

    def get_response(self, uri, status_code, has_data=True, headers=None):
        """Return the response generated from a generic GET request. Do basic
        validation on the response."""
        if headers is None:
            headers = {}
        response = self.app.get(uri, headers=headers)
        assert response.status_code == status_code
        if has_data:
            assert response.data
        return response

    def post_response(self):
        """Return the response generated from a generic POST request. Do basic
        validation on the response."""
        response = self.app.post('/artists',
                content_type='application/json',
                data=json.dumps({u'Name': u'Jeff Knupp'}))
        assert response.status_code == 201
        assert json.loads(response.data)[u'Name'] == u'Jeff Knupp'
        return response

    @staticmethod
    def is_html_response(response):
        """Return True if *response* is an HTML response (TODO: check
        headers as well)."""
        return '<!DOCTYPE html>' in response.data

    def test_get(self):
        """Test simple HTTP GET"""
        response = self.get_response('/artists', 200)
        assert len(json.loads(response.data)[u'resources']) == 275

    def test_post(self):
        """Test simple HTTP POST"""
        response = self.post_response()
        assert json.loads(response.data)[u'Name'] == u'Jeff Knupp'
        assert json.loads(response.data)[u'links'] == [
                {u'rel': u'self', u'uri': u'/artists/276'}
                ]

    def test_posted_location(self):
        """Make sure 'Location' header returned in response actually points to
        new resource created during POST."""
        post_response = self.post_response()
        location = post_response.headers['Location']
        self.get_response(location, 200)

    def test_posted_uri(self):
        """Make sure 'uri' in the links returned in response actually points to
        new resource created during POST."""
        post_response = self.post_response()
        as_json = json.loads(post_response.data)
        uri = as_json[u'links'][0][u'uri']
        self.app.get(uri)
        assert as_json[u'Name'] == u'Jeff Knupp'

    def test_patch_new_resource(self):
        """Send HTTP PATCH for a resource which doesn't exist (should be
        created)."""
        response = self.app.patch('/artists/276',
                content_type='application/json',
                data=json.dumps({u'Name': u'Jeff Knupp'}))
        assert response.status_code == 201
        assert type(response.data) == str
        assert json.loads(response.data)['Name'] == u'Jeff Knupp'
        assert json.loads(response.data)['links'] == [
                {u'rel': u'self', u'uri': u'/artists/276'}]

    def test_patch_existing_resource(self):
        """Send HTTP PATCH for an existing resource (should be updated)."""
        response = self.app.patch('/artists/275',
                content_type='application/json',
                data=json.dumps({u'Name': u'Jeff Knupp'}))
        assert response.status_code == 204
        response = self.get_response('/artists/275', 200)
        assert json.loads(
                response.data.decode('utf-8'))[u'Name'] == u'Jeff Knupp'
        assert json.loads(
                response.data.decode('utf-8'))[u'ArtistId'] == 275

    def test_delete_resource(self):
        """Test DELETEing a resource."""
        response = self.app.delete('/artists/275')
        assert response.status_code == 204
        response = self.get_response('/artists/275', 404, False)

    def test_delete_non_existant_resource(self):
        """Test DELETEing a resource that doesn't exist."""
        response = self.app.delete('/artists/404')
        assert response.status_code == 404

    def test_delete_not_supported(self):
        """Test DELETEing a resource for an endpoint that doesn't support it."""
        response = self.app.delete('/playlists/1')
        assert response.status_code == 403

    def test_unsupported_patch_resource(self):
        """Test PATCHing a resource for an endpoint that doesn't support it."""
        response = self.app.patch('/styles/26',
                content_type='application/json',
                data=json.dumps({u'Name': u'Hip-Hop'}))
        assert response.status_code == 403

    def test_unsupported_get_resource(self):
        """Test GETing a resource for an endpoint that doesn't support it."""
        self.get_response('/playlists', 403, False)

    def test_unsupported_collection_method(self):
        """Test POSTing a collection for an endpoint that doesn't support it."""
        response = self.app.post('/styles',
                content_type='application/json',
                data=json.dumps({u'Name': u'Jeff Knupp'}))
        assert response.status_code == 403

    def test_user_defined_endpoint(self):
        """Make sure user-defined endpoint exists."""
        response = self.get_response('/styles', 200)
        assert len(json.loads(response.data)[u'resources']) == 25

    def test_user_validation_reject(self):
        """Test user-defined validation which on request which should be
        rejected."""
        self.get_response('/styles/1', 403, False)

    def test_user_validation_accept(self):
        """Test user-defined validation which on request which should be
        accepted."""
        self.get_response('/styles/2', 200)

    def test_get_html(self):
        """Test getting HTML version of a resource rather than JSON."""
        response = self.get_response('/artists/1',
                200,
                headers={'Accept': 'text/html'})
        assert self.is_html_response(response)

    def test_get_html_collection(self):
        """Test getting HTML version of a collection rather than JSON."""
        response = self.app.get('/artists',
                200,
                headers={'Accept': 'text/html'})
        assert self.is_html_response(response)
        assert 'Aerosmith' in response.data

    def test_get_json(self):
        """Test explicitly getting the JSON version of a resource."""
        response = self.get_response('/artists',
                200,
                headers={'Accept': 'application/json'})
        assert len(json.loads(response.data)[u'resources']) == 275

    def test_post_html_response(self):
        """Test POSTing a resource and requesting the response be HTML
        formatted."""
        response = self.app.post('/artists',
                content_type='application/json',
                headers={'Accept': 'text/html'},
                data=json.dumps({u'Name': u'Jeff Knupp'}))
        assert response.status_code == 201
        assert 'Jeff Knupp' in response.data

    def test_put_resource(self):
        """Test HTTP PUTing a resource that already exists (should be
        updated)."""
        response = self.app.put('/tracks/1',
                content_type='application/json',
                data=json.dumps(
                    {'Name': 'Some New Album',
                      'AlbumId': 1,
                      'GenreId': 1,
                      'MediaTypeId': 1,
                      'Milliseconds': 343719,
                      'TrackId': 1,
                      'UnitPrice': 0.99,}))
        assert response.status_code == 204
        response = self.get_response('/tracks/1', 200)
        assert json.loads(
                response.data.decode('utf-8'))[u'Name'] == u'Some New Album'
        assert json.loads(
                response.data.decode('utf-8'))[u'Composer'] is None

    def test_put_unknown_resource(self):
        """Test HTTP PUTing a resource that doesn't exist. Should give 404."""
        response = self.app.put('/tracks/99999',
                content_type='application/json',
                data=json.dumps(
                    {'Name': 'Some New Album',
                      'AlbumId': 1,
                      'GenreId': 1,
                      'MediaTypeId': 1,
                      'Milliseconds': 343719,
                      'TrackId': 99999,
                      'UnitPrice': 0.99,}))
        assert response.status_code == 404

    def test_put_invalid_foreign_key(self):
        """Test HTTP PUTing a resource with a field that refers to a
        non-existent resource (i.e. violate a foreign key constraint)."""
        response = self.app.put('/tracks/998',
                content_type='application/json',
                data=json.dumps(
                    {'Name': 'Some New Album',
                      'Milliseconds': 343719,
                      'TrackId': 998,
                      'UnitPrice': 0.99,}))
        assert response.status_code == 422

    def test_put_fail_validation(self):
        """Test HTTP PUTing a resource that fails user-defined validation."""
        response = self.app.put('/tracks/999',
                content_type='application/json',
                data=json.dumps(
                    {'Name': 'Some New Album',
                      'GenreId': 1,
                      'AlbumId': 1,
                      'MediaTypeId': 1,
                      'Milliseconds': 343719,
                      'TrackId': 999,
                      'UnitPrice': 0.99,}))
        assert response.status_code == 403
