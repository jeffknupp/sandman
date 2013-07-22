from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
app = Flask(__name__)
db = SQLAlchemy(app)
Session = sessionmaker(db.engine)
import sandman
