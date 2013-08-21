===========================
The sandman Admin Interface
===========================

Activating the sandman Admin Interface
--------------------------------------

sandman supports an admin interface, much like the default Django admin 
interface. sandman currently uses [Flask-Admin](https://flask-admin.readthedocs.org/en/latest/)
and some SQLAlchemy, erm, alchemy to allow your resources to be 
administered via the admin interface.

Here's a look at the interface generated for the ``chinook`` database's
``Track`` table, listing the information about various music tracks:

![admin interface screenshot](/images/admin_tracks.jpg)

Pretty nice! From here you can directly create, edit, and delete resources. In
the creation and editing forms, objects related via foreign key (e.g. a
``Track``'s associated ``Album``) are auto-populated in a dropdown based on
available values. This ensures that all database constraints are honored when
making changes via the admin.

To activate the admin interface (which adds an ``/admin`` endpoint to your
service, accessible via a browser), you'll need to call one additional function:
``model.activate_admin_classes``. By default, calling this function will make _all_
Models accessible in the admin. If you'd like to prevent this, simply call
``register()`` with ``use_admin=False`` for whichever Model/Models you don't 
want to appear.

Getting Richer Information for Related Objects
----------------------------------------------

The sharp-eyed among you may have noticed that the information presented for
``Album``, ``Genre``, and ``MediaType`` are not very helpful. By default, the
value that will be shown is the value returned by ``__str__`` on the 
associated table. Currently, ``__str__`` simply returns the value of a Model's 
``primary_key()`` attribute. By overriding ``__str__``, however, we can display
more useful information. After making the changes below::

    from sandman.model import register, activate_admin_classes, Model

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
    activate_admin_classes()

Now, we get much more useful information in the columns mentioned, as you can
see here:

![improved admin interface screenshot](/images/admin_tracks_improved.jpg)
