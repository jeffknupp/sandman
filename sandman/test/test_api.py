from sandman import app
from models import Artist, Base
from flask.ext.sqlalchemy import SQLAlchemy
from . import sandman, model
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chinook'
sandman.manager.register((Artist.endpoint, Artist))
app.run(debug=True)
