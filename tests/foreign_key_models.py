"""Test that foreign keys with non-trivial keys are properly ignored."""
from sandman import app
from sandman.model import activate

activate(admin=False, browser=False, reflect_all=True)
