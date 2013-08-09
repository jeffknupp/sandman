===========
Quickstart
===========

Create one file with the following contents (which I call ``runserver.py``)::

    from sandman.model import register, Model

    # Insert Models here
    # Register models here 
    # register((Model1, Model2, Model3))

    from sandman import app, db
    app.config['SQLALCHEMY_DATABASE_URI'] = '<your database connection string (using SQLAlchemy)'
    app.run()

Then simply run::

    python runserver.py

and try curling your new REST API service!

In a "real" project, you should divide the code into at least two files: one with the 
"Model" definitions (``models.py``) and the other with the configuration 
and ``app.run()`` call (``runserver.py``). 

Or you can come up with your own scheme. Whatever.
