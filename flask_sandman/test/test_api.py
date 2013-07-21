from flask import Flask
from flask_sandman.sandman import Sandman
from sandman import sandman
from models import Artist, Base
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
if __name__ == "__main__":
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chinook'
    db = SQLAlchemy(app)
    sandman = Sandman(app, db, {Artist.endpoint, Artist})
    Base.prepare(db.engine)
    app.run(debug=True)
