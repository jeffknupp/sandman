"""Run server"""
from sandman import app, db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chinook'
from models import Artist, Base
from sandman import sandman
sandman.register((Artist.endpoint, Artist))
app.run(debug=True)
