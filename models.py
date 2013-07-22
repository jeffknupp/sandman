from sandman.model import register, Model

class Artist(Model):
    __tablename__ = 'Artist'
    endpoint = 'artists'
    primary_key = 'ArtistId'

class Album(Model):
    __tablename__ = 'Album'
    endpoint = 'albums'
    primary_key = 'AlbumId'

class Playlist(Model):
    __tablename__ = 'Playlist'
    endpoint = 'playlists'
    primary_key = 'PlaylistId'

class Genre(Model):
    __tablename__ = 'Genre'
    endpoint = 'genres'
    primary_key = 'GenreId'

register((Artist, Album, Playlist, Genre))
