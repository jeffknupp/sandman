"""Models"""
from sandman.model import Model

class Artist(Model):
    """Artist model"""
    __tablename__ = 'Artist'
    primary_key = 'artistId'
    endpoint = 'artist'
