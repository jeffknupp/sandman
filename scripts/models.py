from sandman.model import register, Model

class Track(Model):
    __tablename__ = 'Track'

class Artist(Model):
    __tablename__ = 'Artist'

class Album(Model):
    __tablename__ = 'Album'

class Playlist(Model):
    __tablename__ = 'Playlist'

class Genre(Model):
    __tablename__ = 'Genre'

register((Artist, Album, Playlist, Genre, Track))
