sandman
=======

[![Build Status](https://travis-ci.org/jeffknupp/sandman.png?branch=develop)](https://travis-ci.org/jeffknupp/sandman)
[![Coverage Status](https://coveralls.io/repos/jeffknupp/sandman/badge.png?branch=develop)](https://coveralls.io/r/jeffknupp/sandman?branch=develop)
[![Stories in Ready](https://badge.waffle.io/jeffknupp/sandman.png)](http://waffle.io/jeffknupp/sandman)

Documentation
-------------

[Sandman documentation](https://sandman.readthedocs.org/en/latest/)

`sandman` "makes things REST". Have an existing database you'd like to expose via
a REST API? Normally, you'd have to write a ton of boilerplate code for
the ORM you're using, then integrate that into some web framework. 

I don't want to write boilerplate.

Here's what's required to create a RESTful API service from an existing database using
`sandman`:

```python
from `sandman` import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chinook'

from sandman.model import activate

activate()

app.run()
```

That's it! **You don't even need to tell `sandman` what tables your database
contains.** Just point sandman at your database and let it do all the heavy
lifting

Let's start our new service and make a request. While we're at it, lets make use
of Sandman's awesome filtering capability by specifying a filter term:

```zsh
> python runserver.py &
* Running on http://127.0.0.1:5000/

> curl GET "http://localhost:5000/artists?Name=AC/DC"
```

```json
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
```

All of that, including filtering/searching, is automagically available from
those 10 measly lines of code.

Oh, that's not enough? You also want a Django-style admin interface built
automatically? Fine. You may have noticed that when you ran `runserver.py` that
a browser window popped up. Now's the time to go check that out. You'll find
it's that Django-style admin interface you've been bugging me about, looking
something like this:

![admin interface awesomesauce screenshot](/docs/images/admin_tracks_improved.jpg)

If you wanted to specify specific tables that `sandman` should make available,
how do you do that? With this little ditty:

```python
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
```

And if you wanted to add custom logic for an endpoint? Or change the endpoint
name? Or add validation? All supported. Here's a "fancy" class definition:

```python
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
```

With `sandman`, (almost) zero boilerplate code is required. Your existing database
structure and schema is introspected and your database tables magically get a
RESTful API and admin interface. For each table, `sandman` creates:

* proper endpoints 
* support for a configurable set of HTTP verbs 
    * GET
    * POST
    * PATCH
    * PUT
    * DELETE
* responses with appropriate `rel` links automatically
  * foreign keys in your tables are represented by link
* custom validation by simply defining `validate_<METHOD>` methods on your Model
* explicitly list supported methods for a Model by setting the `__methods__` attribute
* customize a Models endpoint by setting the `__endpoint__` method
* essentially a HATEOAS-based service sitting in front of your database

Sandman is under active development but should be usable in any envrionment due
to one simple fact:

**Sandman never alters your database unless you add or change a record yourself.  It adds no extra tables to your existing database and requires no changes to any of your existing tables. If you start sandman, use it to browse your database via cURL, then stop sandman, your database will be in exactly the same state as it was before you began.** 

### Installation

`pip install sandman`

### Quickstart

You'll need to create one file with the following contents (which I call `runserver.py`):

```python
from sandman.model import register, activate, Model

# Insert Models here
# Register models here 
# register((Model1, Model2, Model3)) 
# or
# register(Model1)
# register(Model2)
# register(Model3)

# activate(admin=True)

from sandman import app, db
app.config['SQLALCHEMY_DATABASE_URI'] = '<your database connection string (using SQLAlchemy)>'
app.run()
```

Then simply run 

```bash
python runserver.py
```

and try curling your new RESTful API!

### Example Application

Take a look in the `sandman/test` directory. The application found there makes
use of the [Chinook](http://chinookdatabase.codeplex.com) sample SQL database.

### Coming Soon

* Authentication
