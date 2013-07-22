"""Run server"""
from sandman import app, db
from models import Artist, Base
from sandman import sandman
sandman.register((Artist.endpoint, Artist))
app.run(debug=True)
