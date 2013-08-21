"""Run server"""
from sandman import app, db
import os
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + os.path.abspath(os.path.dirname(__file__)) + '/chinook'
app.secret_key = 's3cr3t'
import models
app.run(debug=True)
