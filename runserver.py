"""Run server"""
from sandman import app, db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chinook'
import models
app.run()
