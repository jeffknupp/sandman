"""Test foreign key edge cases."""

from sandman import app
import os
import shutil
import json

class TestSandmanForeignKeysBase(object):
    """Class to test edge-case foreign key conditions, using a database
    explicitly built to contain these cases."""

    DB_LOCATION = os.path.join(os.getcwd(), 'sandman', 'test', 'foreign_key')

    def setup_method(self, _):
        """Grab the database file from the *data* directory and configure the
        app."""
        shutil.copy(
                os.path.join(
                    os.getcwd(),
                    'sandman',
                    'test',
                    'data',
                    'foreign_key'),
                self.DB_LOCATION)
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + self.DB_LOCATION
        app.config['TESTING'] = True
        self.app = app.test_client()
        # pylint: disable=unused-variable
        from . import foreign_key_models

    def test_get(self):
        """Test simple HTTP GET, enough to cover all cases for now"""
        response = self.app.get('/job_schedules')
        assert len(json.loads(response.data)[u'resources']) == 1

    def teardown_method(self, _):
        """Remove the database file copied during setup."""
        os.unlink(self.DB_LOCATION)
        # pylint: disable=attribute-defined-outside-init
        self.app = None
