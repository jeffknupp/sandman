"""Run server"""
from sandman import app, db
import os
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite+pysqlite:///tests/data/chinook.sqlite3'
app.secret_key = 's3cr3t'
import models
app.run(host='0.0.0.0', debug=True)
