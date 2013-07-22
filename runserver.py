"""Run server"""
from sandman import app, db
from sandman.sandman import register
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chinook'
from models import Artist
register((Artist.endpoint, Artist))
app.run(debug=True)
