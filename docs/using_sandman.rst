=============
Using Sandman
=============

The Simplest Application
------------------------

Here's what's required to create a RESTful API service from an existing database using
``sandman`` ::

    $ sandmanctl sqlite:////tmp/my_database.db

*That's it.* ``sandman`` will then do the following:

* Connect to your database and introspect it's contents
* Create and launch a RESTful API service
* Create an HTML admin interface
* *Open your browser to the admin interface*

That's right. Given a legacy database, ``sandman`` not only gives you a REST API,
it gives you a beautiful admin page and *opens your browser to the admin page*.
It truly does everything for you.

Supported Databases
-------------------

``sandman`` , by default, supports connections to the same set of databases as
SQLAlchemy (http://www.sqlalchemy.org). As of this writing, that includes:

* MySQL (MariaDB)
* PostgreSQL
* SQLite
* Oracle
* Microsoft SQL Server
* Firebird
* Drizzle
* Sybase
* IBM DB2
* SAP Sybase SQL Anywhere
* MonetDB

Beyond `sandmanctl`
-------------------

``sandmanctl``  is really just a simple wrapper around the following::

    from ``sandman`` import app

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chinook'

    from sandman.model import activate

    activate(browser=True)

    app.run()

**Notice you don't even need to tell ``sandman`` what tables your database contains.**
Just point ``sandman`` at your database and let it do all the heavy lifting.

If you put the code above into a file named ``runserver.py``, You can start this new 
service and make a request. While we're at it, lets make use
of ``sandman``'s awesome filtering capability by specifying a filter term::

    $ python runserver.py &
    * Running on http://127.0.0.1:5000/

    > curl GET "http://localhost:5000/artists?Name=AC/DC"

you should see the following::

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

If you were to leave off the filtering term, you would get **all** results from
the ``Artist`` table. You can also *paginate* these results by specifying ``?page=2``
or something similar. The number of results returned per page is controlled by
the config value ``RESULTS_PER_PAGE``, which defaults to 20. 

A Quick Guide to REST APIs
~~~~~~~~~~~~~~~~~~~~~~~~~~

Before we get into more complicated examples, we should discuss some
REST API basics. The most important concept is that of a *resource*.
Resources are sources of information, and the API is an interface to this information.
That is, resources are the actual "objects" manipulated by the API. In ``sandman``, each
row in a database table is considered a resource.

Groups of resources are called *collections*. In ``sandman``, each table in your
database is a collection. Collections can be queried and added to using the
appropriate *HTTP method*. ``sandman`` supports the following HTTP methods::

* GET
* POST
* PUT
* DELETE
* PATCH

(Support for the ``HEAD`` and ``OPTIONS`` methods is underway.)

===============
Creating Models
===============

A ``Model`` represents a table in your database. You control which tables to
expose in the API through the creation of classes which inherit from
:class:`sandman.model.models.Model`. If you create a ``Model``, the only attribute you 
must define in your class is the ``__tablename__`` attribute. ``sandman`` uses this to map your
class to the corresponding database table. From there, ``sandman`` is able to divine
all other properties of your tables. Specifically, ``sandman`` creates the
following:

- an ``__endpoint__`` attribute that controls resource URIs for the class
- a ``__methods__`` attribute that determines the allowed HTTP methods for the class
- ``as_dict`` and ``from_dict`` methods that only operate on class attributes
  that correspond to database columns
- an ``update`` method that updates only the values specified (as opposed to
  ``from_dict``, which replaces all of the object's values with those passed in
  the dictionary parameter
- ``links``, ``primary_key``, and ``resource_uri`` methods that provide access
  to various attributes of the object derived from the underlying database model

Creating a ``models.py`` file allows you to get *even more* out of ``sandman``. In the file,
create a class that derives from ``sandman.models.Model`` for each table you want to
turn into a RESTful resource. Here's a simple example using the Chinook test database
(widely available online)::

    from sandman.model import register, activate, Model

    class Artist(Model):
        __tablename__ = 'Artist'

    class Album(Model):
        __tablename__ = 'Album'

    class Playlist(Model):
        __tablename__ = 'Playlist'

    class Genre(Model):
        __tablename__ = 'Genre'

    # register can be called with an iterable or a single class
    register((Artist, Album, Playlist))
    register(Genre)
    # activate must be called *after* register
    activate(browser=False)


Hooking up Models
-----------------

The ``__tablename__`` attribute is used to tell ``sandman`` which database table
this class is modeling. It has *no default* and is *required* for all classes.

Providing a custom endpoint
---------------------------

In the code above, we created four :class:`sandman.model.models.Model` classes that
correspond to tables in our database. If we wanted to change the HTTP endpoint for
one of the models (the default endpoint is simply the class's name pluralized in lowercase),
we would do so by setting the ``__endpoint__`` attribute in the definition of the class::

    class Genre(Model):
        __tablename__ = 'Genre'
        __endpoint__ = 'styles'

Now we would point our browser (or ``curl``) to ``localhost:5000/styles`` to
retrieve the resources in the ``Genre`` table.

Restricting allowable methods on a resource
-------------------------------------------

Many times, we'd like to specify that certain actions can only be carried out
against certain types of resources. If we wanted to prevent API users from
deleting any ``Genre`` resources, for example, we could specify this implicitly
by defining the ``__methods__`` attribute and leaving out the ``DELETE`` method,
like so::

    class Genre(Model):
        __tablename__ = 'Genre'
        __endpoint__ = 'styles'
        __methods__ = ('GET', 'POST', 'PATCH', 'PUT')

For each call into the API, the HTTP method used is validated against the
acceptable methods for that resource.

Performing custom validation on a resource
------------------------------------------

Specifying which HTTP methods are acceptable gives rather coarse control over
how a user of the API can interact with our resources. For more granular
control, custom a validation function can be specified. To do so, simply define a
static method named ``validate_<METHOD>``, where ``<METHOD>`` is the HTTP method
the validation function should validate. To validate the ``POST`` method on
``Genres``, we would define the method ``validate_POST``, like so::


    class Genre(Model):
        __tablename__ = 'Genre'
        __endpoint__ = 'styles'
        __methods__ = ('GET', 'POST', 'PATCH', 'PUT')

        @staticmethod
        def validate_POST(self, resource=None):
            if isinstance(resource, list):
                return True

            # No classical music!
            return resource and resource.Name != 'classical'

The ``validate_POST`` method is called *after* the would-be resource is created,
trading a bit of performance for a simpler interface. Instead of needing to
inspect the incoming HTTP request directly, you can make validation decisions
based on the resource itself.

Note that the ``resource`` parameter can be either a single resource or a
collection of resources, so it's usually necessary to check which type you're
dealing with. This will likely change in a future version of sandman.

Configuring a model's behavior in the admin interface
-----------------------------------------------------

``sandman`` uses `Flask-Admin` to construct the admin interface. While the default
settings for individual models are usually sufficient, you can make changes to the
admin interface for a model by setting the `__view__` attribute to a class that derives
from `flask.ext.admin.contrib.sqla.ModelView`. The Flask-Admin's documentation should be
consulted for the full list of attributes that can be configured.

Below, we create a model and, additionally, tell ``sandman`` that we want the table's
primary key to be displayed in the admin interface (by default, a table's primary keys
aren't shown)::

  from flask.ext.admin.contrib.sqla import ModelView

  class ModelViewShowPK(ModelView):

    column_display_pk = True

  class Artist(Model):
    __tablename__ = 'Artist'
    __view__ = ModelViewShowPK

**Custom `__view__` classes are a powerful way to customize the admin interface.**
Properties exist to control which columns are sortable or searchable, as well
as as what fields are editable in the built-in editing view. If you find your
admin page isn't working exactly as you'd like, the chances are good you can
add your desired functionality through a custom `__view__` class.


===============
Model Endpoints
===============

If you were to create a ``Model`` class named ``Resource``, the following endpoints would be created:

* ``resources/``
    * ``GET``: retrieve all resources (i.e. the *collection*)
    * ``POST``: create a new resource
* ``resources/<id>``
    * ``GET``: retrieve a specific resource
    * ``PATCH``: update an existing resource
    * ``PUT``: create or update a resource with the given ID
    * ``DELETE``: delete a specific resource
* ``resources/meta``
    * ``GET``: retrieve a description of a resource's structure

The root endpoint
-----------------

For each project, a "root" endpoint (``/``) is created that gives clients
the information required to interact with your API. The endpoint for each
resource is listed, along with the ``/meta`` endpoint describing a resource's
structure.

The root endpoint is available as both JSON and HTML. The same information is
returned by each version.

The ``/meta`` endpoint
----------------------

A ``/meta`` endpoint, which lists the models attributes (i.e. the database
columns) and their type. This can be used to create client code that is 
decoupled from the structure of your database. 

A ``/meta`` endpoint is automatically generated for every ``Model`` you register.
This is available both as JSON and HTML.

=======================
Automatic Introspection
=======================

Of course, you don't actually need to tell ``sandman`` about your tables; it's
perfectly capable of introspecting all of them. To use introspection to make
*all* of your database tables available via the admin and REST API, simply
remove all model code and call `activate()` without ever registering a model.
To stop a browser window from automatically popping up on sandman
initialization, call `activate()` with `browser=False`.

=========================================
Running ``sandman`` alongside another app
=========================================

If you have an existing WSGI application you'd like to run in the same
interpreter as ``sandman``, follow the instructions described here_.
Essentially, you need to import both applications in your main file and use
Flask's ``DispatcherMiddleware`` to give a unique route to each app. In the
following example, ``sandman``-related endpoints can be accessed by adding the
``/sandman`` prefix to ``sandman``'s normally generated URIs::

    from my_application import app as my_app
    from sandman import app as sandman_app
    from werkzeug.wsgi import DispatcherMiddleware

    application = DispatcherMiddleware(my_app, {
        '/sandman': sandman_app,
        })

This allows both apps to coexist; ``my_app`` will be rooted at ``/`` and
``sandman`` at ``/sandman``.

Using existing declarative models
---------------------------------

If you have a Flask/SQLAlchemy application that already has a number of existing
declarative models, you can register these with ``sandman`` as if they were
auto-generated classes. Simply add your existing classes in the call to :func:`sandman.model.register`

.. _here: http://flask.pocoo.org/docs/patterns/appdispatch/#app-dispatch
