sandman
=======

|Build Status|

|Coverage Status|

|Gitter chat|

|Analytics|

|PyPI|

Homepage
--------

Visit the home of ``sandman`` on the web:
`sandman.io <http://www.sandman.io>`__

Discuss
-------

Looking for a place to ask questions about sandman? Check out the
sandman-discuss and sandman-users forums!

Documentation
-------------

`Sandman documentation <https://sandman.readthedocs.org/en/latest/>`__

``sandman`` "makes things REST". Have an existing database you'd like to
expose via a REST API? Normally, you'd have to write a ton of
boilerplate code for the ORM you're using, then integrate that into some
web framework.

I don't want to write boilerplate.

Here's what's required to create a RESTful API service from an existing
database using ``sandman``:

.. code:: bash

    $ sandmanctl sqlite:////tmp/my_database.db

*That's it.* ``sandman`` will then do the following:

-  connect to your database and introspect its contents
-  create and launch a REST API service
-  create an HTML admin interface
-  *open your browser to the admin interface*

That's right. Given a legacy database, ``sandman`` not only gives you a
REST API, it gives you a beautiful admin page and *opens your browser to
the admin page*. It truly does everything for you.

Supported Databases
-------------------

``sandman``, by default, supports connections to the same set of
databases as `SQLAlchemy <http://www.sqlalchemy.org>`__. As of this
writing, that includes:

-  MySQL (MariaDB)
-  PostgreSQL
-  SQLite
-  Oracle
-  Microsoft SQL Server
-  Firebird
-  Drizzle
-  Sybase
-  IBM DB2
-  SAP Sybase SQL Anywhere
-  MonetDB

Behind the Scenes
-----------------

``sandmanctl`` is really just a simple wrapper around the following:

.. code:: python

    from sandman import app

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chinook'

    from sandman.model import activate

    activate()

    app.run()

**You don't even need to tell ``sandman`` what tables your database
contains.** Just point ``sandman`` at your database and let it do all
the heavy lifting

Let's start our new service and make a request. While we're at it, lets
make use of ``sandman``'s awesome filtering capability by specifying a
filter term:

.. code:: zsh

    > python runserver.py &
    * Running on http://127.0.0.1:5000/

    > curl GET "http://localhost:5000/artists?Name=AC/DC"

.. code:: json

    ...
    {
        "resources": [
            {
                "ArtistId": 1,
                "Name": "AC/DC",
                "links": [
                    {
                        "rel": "self",
                        "uri": "/artists/1"
                    }
                ]
            }
        ]
    }

All of that, including filtering/searching, is automagically available
from those *five* measly lines of code.

Oh, that's not enough? You also want a Django-style admin interface
built automatically? Fine. You may have noticed that when you ran
``runserver.py`` that a browser window popped up. Now's the time to go
check that out. You'll find it's that Django-style admin interface
you've been bugging me about, looking something like this:

.. figure:: /docs/images/admin_tracks_improved.jpg
   :alt: admin interface awesomesauce screenshot

   admin interface awesomesauce screenshot
(If you want to disable the browser from opening automatically each time
``sandman`` starts, call ``activate`` with ``browser=False``)

If you wanted to specify specific tables that ``sandman`` should make
available, how do you do that? With this little ditty:

.. code:: python

    from sandman.model import register, Model

    class Artist(Model):
        __tablename__ = 'Artist'

    class Album(Model):
        __tablename__ = 'Album'

    class Playlist(Model):
        __tablename__ = 'Playlist'

    register((Artist, Album, Playlist))

And if you wanted to add custom logic for an endpoint? Or change the
endpoint name? Or add validation? All supported. Here's a "fancy" class
definition:

.. code:: python

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

With ``sandman``, zero boilerplate code is required. In fact, using
``sandmanctl``, **no code is required at all**. Your existing database
structure and schema is introspected and your database tables magically
get a RESTful API and admin interface. For each table, ``sandman``
creates:

-  proper endpoints
-  support for a configurable set of HTTP verbs

   -  GET
   -  POST
   -  PATCH
   -  PUT
   -  DELETE

-  responses with appropriate ``rel`` links automatically
-  foreign keys in your tables are represented by link
-  custom validation by simply defining ``validate_<METHOD>`` methods on
   your Model
-  explicitly list supported methods for a Model by setting the
   ``__methods__`` attribute
-  customize a Models endpoint by setting the ``__endpoint__`` method
-  essentially a HATEOAS-based service sitting in front of your database

``sandman`` is under active development but should be usable in any
environment due to one simple fact:

**``sandman`` never alters your database unless you add or change a
record yourself. It adds no extra tables to your existing database and
requires no changes to any of your existing tables. If you start
``sandman``, use it to browse your database via cURL, then stop
``sandman``, your database will be in exactly the same state as it was
before you began.**

Installation
~~~~~~~~~~~~

``pip install sandman``

Example Application
~~~~~~~~~~~~~~~~~~~

Take a look in the ``sandman/test`` directory. The application found
there makes use of the `Chinook <http://chinookdatabase.codeplex.com>`__
sample SQL database.

Contact Me
----------

Questions or comments about ``sandman``? Hit me up at
jeff@jeffknupp.com.

Coming Soon
~~~~~~~~~~~

-  Authentication

|Bitdeli Badge|

.. |Build Status| image:: https://travis-ci.org/jeffknupp/sandman.png?branch=develop
   :target: https://travis-ci.org/jeffknupp/sandman
.. |Coverage Status| image:: https://coveralls.io/repos/jeffknupp/sandman/badge.png?branch=develop
   :target: https://coveralls.io/r/jeffknupp/sandman?branch=develop
.. |Gitter chat| image:: https://badges.gitter.im/jeffknupp/sandman.png
   :target: https://gitter.im/jeffknupp/sandman
.. |Analytics| image:: https://ga-beacon.appspot.com/UA-12615441-7/sandman/home
   :target: https://github.com/jeffknupp/sandman
.. |PyPI| image:: http://img.shields.io/pypi/dm/sandman.svg
   :target: http://img.shields.io/pypi/dm/sandman.svg
.. |Bitdeli Badge| image:: https://d2weczhvl823v0.cloudfront.net/jeffknupp/sandman/trend.png
   :target: https://bitdeli.com/free
