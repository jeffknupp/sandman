from sandman.model import register, Model

class Artist(Model):
    __tablename__ = 'Artist'

class Album(Model):
    __tablename__ = 'Album'

class Playlist(Model):
    __tablename__ = 'Playlist'

class Genre(Model):
    __tablename__ = 'Genre'
    __endpoint__ = 'styles'

register((Artist, Album, Playlist, Genre))
