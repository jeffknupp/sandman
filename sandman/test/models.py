from sandman.model import register, Model

class Artist(Model):
    __tablename__ = 'Artist'
    endpoint = 'artists'

class Album(Model):
    __tablename__ = 'Album'
    endpoint = 'albums'

class Playlist(Model):
    __tablename__ = 'Playlist'
    endpoint = 'playlists'

class Genre(Model):
    __tablename__ = 'Genre'
    endpoint = 'genres'

register((Artist, Album, Playlist, Genre))
