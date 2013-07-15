"""Run server"""
from sandman import app, db
import os
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + os.path.abspath(os.path.dirname(__file__)) + '/chinook'
import models
app.run(debug=True)
