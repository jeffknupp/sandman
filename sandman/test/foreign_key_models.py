"""Test that foreign keys with non-trivial keys are properly ignored."""
from sandman import app
from sandman.model import activate

app.config['SANDMAN_ALL_PRIMARY'] = True
activate(admin=False, browser=False)
