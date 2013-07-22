from sandman.model import register, Model

class Artist(Model):
    __tablename__ = 'Artist'
    primary_key = 'artistId'
    endpoint = 'artists'

register(Artist)
