===========================
The sandman Admin Interface
===========================

Activating the sandman Admin Interface
--------------------------------------

sandman supports an admin interface, much like the Django admin
interface. ``sandman`` currently uses [Flask-Admin](https://flask-admin.readthedocs.org/en/latest/)
and some SQLAlchemy, erm, alchemy to allow your resources to be
administered via the admin interface. Note, though, that the admin
interface may drastically change in the future.

Here's a look at the interface generated for the ``chinook`` database's
``Track`` table, listing the information about various music tracks:

.. image:: images/admin_tracks.jpg

Pretty nice! From here you can directly create, edit, and delete resources. In
the "create" and "edit" forms, objects related via foreign key (e.g. a
``Track``'s associated ``Album``) are auto-populated in a dropdown based on
available values. This ensures that all database constraints are honored when
making changes via the admin.

The admin interface (which adds an ``/admin`` endpoint to your
service, accessible via a browser), is enabled by default. To disable it, pass
``admin=False`` as an argument in your call to ``activate``.
By default, calling this function will make _all_ Models accessible in the admin.
If you'd like to prevent this, simply call ``register()`` with ``use_admin=False``
for whichever Model/Models you don't want to appear. Alternatively, you can
control if a model is viewable, editable, creatable, etc in the admin by
setting your class's ``__view__`` attribute to your own ``Admin`` class.

Getting Richer Information for Related Objects
----------------------------------------------

The sharp-eyed among you may have noticed that the information presented for
``Album``, ``Genre``, and ``MediaType`` are not very helpful. By default, the
value that will be shown is the value returned by ``__str__`` on the
associated table. Currently, ``__str__`` simply returns the value of a Model's
``primary_key()`` attribute. By overriding ``__str__``, however, we can display
more useful information. After making the changes below::

    from sandman.model import register, Model

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
            return self.Id

    class Genre(Model):
        __tablename__ = 'Genre'

        def __str__(self):
            return self.Name

    class MediaType(Model):
        __tablename__ = 'MediaType'

        def __str__(self):
            return self.Name

    register((Artist, Album, Playlist, Genre, Track, MediaType))

we get much more useful information in the columns mentioned, as you can
see here:

.. image:: images/admin_tracks_improved.jpg
