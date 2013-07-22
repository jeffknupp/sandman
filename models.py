from sandman.model import Resource, Base
from sqlalchemy.ext.declarative import DeferredReflection
class Artist(DeferredReflection, Base, Resource):
    __tablename__ = 'Artist'
    primary_key = 'artistId'
    endpoint = 'artists'
