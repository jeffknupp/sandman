from sandman.model import Resource, Base

class Artist(Base, Resource):
    __tablename__ = 'Artist'
    primary_key = 'artistId'
    endpoint = 'artists'
