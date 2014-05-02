from __future__ import absolute_import

from flask import Flask

app = None

def get_app(name, sqlalchemy_uri):
    """Return an instance of a Flask application with the name *name* and
    connected to the DB specified by *sqlalchemy_uri*."""
    global app
    app = Flask(name)
    app.config['SQLALCHEMY_DATABASE_URI'] = sqlalchemy_uri
    app.secret_key = 42
    from sandman.model.models import db
    db.init_app(app)
    return app
