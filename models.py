from sandman.model import Resource
from sandman import db
from sqlalchemy.ext.declarative import declarative_base, DeferredReflection
Base = declarative_base(cls=DeferredReflection)

class Artist(Base, Resource):
    __tablename__ = 'Artist'
    primary_key = 'artistId'
    endpoint = 'artists'

Base.prepare(db.engine)
