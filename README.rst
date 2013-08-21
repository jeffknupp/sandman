sandman
=======

|Build Status| |Coverage Status|

Documentation
-------------

`Sandman documentation <https://sandman.readthedocs.org/en/latest/>`__

**sandman** "makes things REST". Have an existing database you'd like to
expose via a REST API? Normally, you'd have to write a ton of
boilerplate code for the ORM you're using, then integrate that into some
web framework.

I don't want to write boilerplate.

Here's what's required to create a RESTful API service from an existing
database using **sandman**:

.. code:: python

    from sandman import app, db

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chinook'

    from sandman.model import register, Model

    class Artist(Model):
        __tablename__ = 'Artist'

    class Album(Model):
        __tablename__ = 'Album'

    class Playlist(Model):
        __tablename__ = 'Playlist'

    register((Artist, Album, Playlist))

    app.run()

Let's start our new service and make a request:

.. code:: zsh

    > python runserver.py &
    * Running on http://127.0.0.1:5000/

    > curl GET http://localhost:5000/artists

.. code:: json

    ...
    {
        "ArtistId": 273,
        "Name": "C. Monteverdi, Nigel Rogers - Chiaroscuro; London Baroque; London Cornett & Sackbu",
        "links": [
        {
            "rel": "self",
            "uri": "/artists/ArtistId"
        }
        ]
    },
    {
        "ArtistId": 274,
        "Name": "Nash Ensemble",
        "links": [
        {
            "rel": "self",
            "uri": "/artists/ArtistId"
        }
        ]
    },
    {
        "ArtistId": 275,
        "Name": "Philip Glass Ensemble",
        "links": [
        {
            "rel": "self",
            "uri": "/artists/ArtistId"
        }
        ]
    }
    ]

Oh, that's not enough? You also want a Django-style admin interface
built automatically? Fine. Add one more line to the list of models to
get access to this:

.. figure:: /docs/images/admin_tracks_improved.jpg
   :alt: improved admin interface screenshot

   improved admin interface screenshot
With **sandman**, (almost) zero boilerplate code is required. Your
existing database structure and schema is introspected and your database
tables magically get a RESTful API and admin interface. For each table,
Sandman creates:

-  proper endpoints
-  support for a configurable set of HTTP verbs

   -  GET
   -  POST
   -  PATCH
   -  PUT
   -  DELETE

-  responses with appropriate ``rel`` links automatically
-  custom validation by simply defining ``validate_<METHOD>`` methods on
   your Model
-  explicitly list supported methods for a Model by setting the
   ``__methods__`` attribute
-  customize a Models endpoint by setting the ``__endpoint__`` method
-  essentially a HATEOAS-based service sitting in front of your database

*Warning: Sandman is still very much a work in progress. Use it at your
own risk. It's also often changing in backwards incompatible ways.*

Installation
~~~~~~~~~~~~

``pip install sandman``

Quickstart
~~~~~~~~~~

You'll need to create one file with the following contents (which I call
``runserver.py``):

.. code:: python

    from sandman.model import register, Model

    # Insert Models here
    # Register models here 
    # register((Model1, Model2, Model3)) 
    # or
    # register(Model1)
    # register(Model2)
    # register(Model3)

    from sandman import app, db
    app.config['SQLALCHEMY_DATABASE_URI'] = '<your database connection string (using SQLAlchemy)>'
    app.run()

Then simply run

.. code:: bash

    python runserver.py

and try curling your new RESTful API!

Example Application
~~~~~~~~~~~~~~~~~~~

Take a look in the ``sandman/test`` directory. The application found
there makes use of the `Chinook <http://chinookdatabase.codeplex.com>`__
sample SQL database.

Coming Soon
~~~~~~~~~~~

-  Authentication
-  More ``links`` automatically generated (i.e. ``links`` to related
   objects)

.. |Build Status| image:: https://travis-ci.org/jeffknupp/sandman.png?branch=develop
   :target: https://travis-ci.org/jeffknupp/sandman
.. |Coverage Status| image:: https://coveralls.io/repos/jeffknupp/sandman/badge.png?branch=develop
   :target: https://coveralls.io/r/jeffknupp/sandman?branch=develop
