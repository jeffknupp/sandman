"""Test foreign key edge cases."""
import os
import shutil
import json

from sandman import app


class TestSandmanForeignKeysBase(object):
    """Class to test edge-case foreign key conditions, using a database
    explicitly built to contain these cases."""

    DB_LOCATION = os.path.join(os.getcwd(), 'tests', 'foreign_key.sqlite3')

    def setup_method(self, _):
        """Grab the database file from the *data* directory and configure the
        app."""
        shutil.copy(
                os.path.join(
                    os.getcwd(),
                    'tests',
                    'data',
                    'foreign_key.sqlite3'),
                self.DB_LOCATION)
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + self.DB_LOCATION
        app.config['SANDMAN_SHOW_PKS'] = False
        app.config['SANDMAN_GENERATE_PKS'] = True
        app.config['TESTING'] = True
        self.app = app.test_client()
        # pylint: disable=unused-variable
        from . import foreign_key_models

    def test_get(self):
        """Test simple HTTP GET, enough to cover all cases for now."""
        response = self.app.get('/job_schedules')
        assert len(json.loads(response.get_data(as_text=True))[u'resources']) == 1

    def test_date_time(self):
        """Test serializing a datetime object works properly."""
        response = self.app.get('/date_times')
        assert len(json.loads(response.get_data(as_text=True))[u'resources']) == 1
        
    def teardown_method(self, _):
        """Remove the database file copied during setup."""
        os.unlink(self.DB_LOCATION)
        # pylint: disable=attribute-defined-outside-init
        self.app = None
