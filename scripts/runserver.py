"""Run server"""
from sandman import app, db
from sandman.admin import AdminModel, Admin
import os
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite+pysqlite:///tests/data/existing.sqlite3'
app.secret_key = 's3cr3t'
import models
print app.url_map

app.run(host='0.0.0.0', debug=True)
