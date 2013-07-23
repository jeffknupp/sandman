sandman
=======
[![Build Status](https://travis-ci.org/jeffknupp/sandman.png)](https://travis-ci.org/jeffknupp/sandman)

**sandman** "makes things REST". Have an existing database you'd like to expose via
a REST API? Normally, you'd have to write a ton of boilerplate code, likely for
an ORM. This fact alone stops many projects before they begin.

Here's what's required to create a REST API from an existing database using
**sandman**:

```python
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

register((Artist, Album, Playlist))

from sandman import app, db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chinook'
app.run()
```

Let's start our new API server and make a request:

```zsh
/home/jeff/sandman >>> python runserver.py &
* Running on http://127.0.0.1:5000/

/home/jeff/sandman >>> curl GET http://localhost:5000/artists
```

```json
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
```

With **sandman**, (almost) zero boilerplate code is required. Your existing database
structure and schema is introspected and your database tables magically get a
RESTful API. For each table, Sandman creates:

* proper endpoints 
* support for a configurable set of HTTP verbs 
    * GET
    * POST
    * PATCH
    * DELETE
* responses with appropriate `rel` links automatically
* essentially a HATEOAS service sitting in front of your database

*Warning: Sandman is still very much a work in progress and is not suitable for
use **anywhere.** Don't use it for anything important. It's also often changing 
in backwards incompatible ways.*

### Installation

For now, just `git clone` the sandman repo and run `python setup.py install`. 

### Quickstart

You'll need to create one file with the following contents (which I call `runserver.py`):

```python
from sandman.model import register, Model

# Insert Models here
# Register models here 
# register((Model1, Model2, Model3))

from sandman import app, db
app.config['SQLALCHEMY_DATABASE_URI'] = '<your database connection string (using SQLAlchemy)'
app.run()
```

Then simply run 

```bash
python runserver.py
```

and try curling your new REST API service!
