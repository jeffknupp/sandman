"""Models for unit testing sandman"""

from sandman.model import register, Model, activate

class Artist(Model):
    """Model mapped to the "Artist" table"""
    __tablename__ = 'Artist'

class MediaType(Model):
    """Model mapped to the "MediaType" table"""
    __tablename__ = 'MediaType'

    def __str__(self):
        return self.Name

class Track(Model):
    """Model mapped to the "Artist" table"""
    __tablename__ = 'Track'

    @staticmethod
    def validate_PUT(resource=None):
        """Return False if request should not be processed.

        :param resource: resource related to current request
        :type resource: :class:`sandman.model.Model` or None

        """
        if int(resource.TrackId) == 999:
            return False
        return True

class Album(Model):
    """Model mapped to the "Album" table

    Only supports HTTP methods specified.

    """

    __tablename__ = 'Album'
    __methods__ = ('POST', 'PATCH', 'DELETE', 'PUT', 'GET')

    def __str__(self):
        return self.Title

class Playlist(Model):
    """Model mapped to the "Playlist" table

    Only supports HTTP methods specified.

    """

    __tablename__ = 'Playlist'
    __methods__ = ('POST', 'PATCH')

class Style(Model):
    """Model mapped to the "Genre" table

    Has a custom endpoint ("styles" rather than the default, "genres").
    Only supports HTTP methods specified.
    Has a custom validator for the GET method.

    """

    __tablename__ = 'Genre'
    __endpoint__ = 'styles'
    __methods__ = ('GET', 'DELETE')

    @staticmethod
    def validate_GET(resource=None):
        """Return False if the request should not be processed.

        :param resource: resource related to current request
        :type resource: :class:`sandman.model.Model` or None

        """

        if isinstance(resource, list):
            return True
        elif resource and resource.GenreId == 1:
            return False
        return True

register((Artist, Album, Playlist, Track, MediaType))
register(Style)
activate()
