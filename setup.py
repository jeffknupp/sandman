"""
sandman
-------

**sandman** "makes things REST". Have an existing database you'd like to expose via
a REST API? Normally, you'd have to write a ton of boilerplate code for
the ORM you're using. 

We're programmers. We don't write boilerplate.

Simple Setup
````````````

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

Let's start our new API server and make a request.

.. code:: bash

    $ python runserver.py &
    * Running on http://127.0.0.1:5000/

    $ curl GET http://localhost:5000/artists

Here is the JSON returned:

.. code:: json

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

Batteries Included
``````````````````

With **sandman**, (almost) zero boilerplate code is required. Your existing database
structure and schema is introspected and your database tables magically get a
RESTful API. For each table, Sandman creates:

- proper endpoints 
 
- support for a configurable set of HTTP verbs 
     
    - GET

    - POST

    - PATCH

    - DELETE

- responses with appropriate ``rel`` links automatically

- essentially a HATEOAS-based service sitting in front of your database

*Warning: Sandman is still very much a work in progress.* It is not suitable for
use **anywhere.** Don't use it for anything important. It's also often changing 
in backwards incompatible ways.

Links
`````

* `website <http://www.github.com/jeffknupp/sandman/>`_
* `documentation <http://pythonhosted.org/sandman/>`_

"""

from __future__ import print_function
from setuptools import setup

setup(
    name='sandman',
    version='0.2.3.2',
    url='http://github.com/jeffknupp/sandman/',
    license='Apache Software License',
    author='Jeff Knupp',
    author_email='jeff@jeffknupp.com',
    description='Automated REST APIs for existing database-driven systems',
    long_description=__doc__,
    packages=['sandman', 'sandman.test'],
    include_package_data=True,
    platforms='any',
    test_suite='sandman.test.test_sandman',
    classifiers = [
        'Programming Language :: Python',
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        ],
)
