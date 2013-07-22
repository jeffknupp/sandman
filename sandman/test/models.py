from sandman import model

class Artist(model.Base, model.Resource):
    __tablename__ = 'Artist'
    primary_key = 'artistId'
    endpoint = 'artist'
