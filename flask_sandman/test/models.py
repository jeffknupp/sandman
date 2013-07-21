from flask_sandman import model
from sqlalchemy.ext.declarative import declarative_base, DeferredReflection

Base = declarative_base(cls=DeferredReflection)

class Artist(Base, model.Resource):
    __tablename__ = 'Artist'
    primary_key = 'artistId'
    endpoint = 'artist'
