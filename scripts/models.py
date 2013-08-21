from sandman.model import register, activate_admin_classes, Model

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

class MediaType(Model):
    __tablename__ = 'MediaType'

register((Artist, Album, Playlist, Genre, Track, MediaType))
activate_admin_classes()
