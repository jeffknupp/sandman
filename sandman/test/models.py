from sandman.model import register, Model

class Artist(Model):
    __tablename__ = 'Artist'


class Track(Model):
    __tablename__ = 'Track'

    @staticmethod
    def validate_PUT(resource=None):
        if int(resource.TrackId) == 999:
            return False
        return True

class Album(Model):
    __tablename__ = 'Album'
    __methods__ = ('POST', 'PATCH', 'DELETE', 'PUT', 'GET')

class Playlist(Model):
    __tablename__ = 'Playlist'
    __methods__ = ('POST', 'PATCH')

class Genre(Model):
    __tablename__ = 'Genre'
    __endpoint__ = 'styles'
    __methods__ = ('GET', 'DELETE')

    @staticmethod
    def validate_GET(resource=None):
        if isinstance(resource, list):
            return True
        elif resource and resource.GenreId == 1:
            return False
        return True

register((Artist, Album, Playlist, Track))
register(Genre)
