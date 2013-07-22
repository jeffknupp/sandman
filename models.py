from sandman.model import Resource
from sandman import db
from sqlalchemy.ext.declarative import declarative_base, DeferredReflection
Base = declarative_base()

class Artist(DeferredReflection, Base, Resource):
    __tablename__ = 'Artist'
    primary_key = 'artistId'
    endpoint = 'artists'

DeferredReflection.prepare(db.engine)
