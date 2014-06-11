"""Sandman automatically generates a REST API from your existing database,
without you needing to tediously define the tables in typical ORM style. Simply
create a class for each table you want to expose in the API, give it's
associated database table, and off you go! The generated API essentially exposes
a completely new system based on your existing data, using HATEOAS."""
import os

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.httpauth import HTTPBasicAuth

app = Flask(__name__)
app.secret_key = '42'
db = SQLAlchemy(app)
auth = HTTPBasicAuth()
from . import sandman

@app.route('/static/js/<path:path>')
def js_proxy(path):
    # send_static_file will guess the correct MIME type
    return app.send_static_file(os.path.join('js', path))

@app.route('/static/css/<path:path>')
def css_proxy(path):
    # send_static_file will guess the correct MIME type
    return app.send_static_file(os.path.join('css', path))

@app.route('/static/img/<path:path>')
def img_proxy(path):
    # send_static_file will guess the correct MIME type
    return app.send_static_file(os.path.join('img', path))




__version__ = '0.9.6'
