from sandman.model import register, prepare_relationships, activate_admin_classes, Model
from sqlalchemy.orm import relationship

class Track(Model):
    __tablename__ = 'Track'

    def __str__(self):
        return self.Name

class Artist(Model):
    __tablename__ = 'Artist'
    def __str__(self):
        return self.Name

class Album(Model):
    __tablename__ = 'Album'
    def __str__(self):
        return self.Title

class Playlist(Model):
    __tablename__ = 'Playlist'
    def __str__(self):
        return self.Name

class Genre(Model):
    __tablename__ = 'Genre'
    def __str__(self):
        return self.Name


register((Artist, Album, Playlist, Genre, Track))
activate_admin_classes()
prepare_relationships()
