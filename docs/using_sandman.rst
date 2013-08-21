=============
Using Sandman
=============

The Simplest Application
------------------------

We'll be using a subset of the Chinook test database as an example. 
Create one file with the following contents (which I'll call ``runserver.py``)::

    from sandman.model import register, Model
   
    class Artist(Model):
        __tablename__ = 'Artist'

    class Album(Model):
        __tablename__ = 'Album'

    class Playlist(Model):
        __tablename__ = 'Playlist'

    class Genre(Model):
        __tablename__ = 'Genre'

    register((Artist, Album, Playlist))
    register(Genre)

    from sandman import app, db
    app.config['SQLALCHEMY_DATABASE_URI'] = '<your database connection string (using SQLAlchemy)'
    app.run()

Then simply run::

    python runserver.py

and try curling your new REST API service!

A Quick Guide to REST APIs
~~~~~~~~~~~~~~~~~~~~~~~~~~

Before we discuss the example code above in more detail, we should discuss some
REST API basics first. The most important concept is that of a *resource*.
Resources are sources of information, and the API is an interface to this information. 
That is, resources are the actual "objects" manipulated by the API. In sandman, each 
row in a database table is considered a resource. 
Even though the example above is short, let's walk through it step by step.

Creating Models
---------------

A ``Model`` represents a table in your database. You control which tables to
expose in the API through the creation of classes which inherit from 
:class:`sandman.model.models.Model`. The only attribute you must define in your 
class is the ``__tablename__`` attribute. sandman uses this to map your
class to the corresponding database table. From there, sandman is able to divine
all other properties of your tables. Specifically, sandman creates the
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

Customizing Your Resources
------------------------------------------

Providing a custom endpoint
~~~~~~~~~~~~~~~~~~~~~~~~~~~

In the code above, we created 4 :class:`sandman.model.models.Model` classes that
correspond to tables in our database. If we wanted to change the endpoint for a
class (the default endpoint is simply the class's name pluralized), we would do
so by setting the ``__endpoint__`` attribute in the definition of the class::

    class Genre(Model):
        __tablename__ = 'Genre'
        __endpoint__ = 'styles'

Now we would point our browser (or ``curl``) to ``localhost:5000/styles`` to
retrieve the resources in the ``Genre`` table.

Restricting allowable methods on a resource
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Many times, we'd like to specify that certain actions can only be carried out
against certain types of resources. If we wanted to prevent API users from
deleting any ``Genre`` resources, for example, we could specify this implicitly
by defining the ``__methods__`` attribute and leaving it out, like so::


    class Genre(Model):
        __tablename__ = 'Genre'
        __endpoint__ = 'styles'
        __methods__ = ('GET', 'POST', 'PATCH', 'PUT')

For each call into the API, the HTTP method used is validated against the
acceptable methods for that resource. 

Performing custom validation on a resource
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Specifying which HTTP methods are acceptable gives rather coarse control over
how a user of the API can interact with our resources. For more granular
control, custom validation functions can be specified. To do so, simply define a
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

Project Layout
--------------

In a "real" project, you should divide the code into at least two files: one with the 
``Model`` definitions (``models.py``) and the other with the configuration 
and the ``app.run()`` call (``runserver.py``). 
