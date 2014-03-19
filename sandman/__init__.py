"""Sandman automatically generates a REST API from your existing database,
without you needing to tediously define the tables in typical ORM style. Simply
create a class for each table you want to expose in the API, give it's
associated database table, and off you go! The generated API essentially exposes
a completely new system based on your existing data, using HATEOAS."""

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.secret_key = '42'
db = SQLAlchemy(app)
from . import sandman

__version__ = '0.7.7'
