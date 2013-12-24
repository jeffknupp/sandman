"""Script to run sandman via command line

Usage:
    sandmanctl.py URI

Start sandman and connect to database at URI

Supported database dialects:

[PostgreSQL]
[MySQL]
[Oracle]
[Microsoft SQL Server]
[SQLite]
[Drizzle]
[Firebird]
[Sybase]

External dialects and packages:

[IBM DB2]: ibm_db_sa
[SAP Sybase SQL Anywhere]: sqlalchemy-sqlany
[MonetDB]: sqlalchemy-monetdb

Arguments:
    URI     RFC-1738 style database URI

Options:
    -h --help   Show this screen.

'postgresql+psycopg2://scott:tiger@localhost/test'

"""
from __future__ import absolute_import

from docopt import docopt

from sandman import app
from sandman.model import activate

def main():
    options = docopt(__doc__)
    app.config['SQLALCHEMY_DATABASE_URI'] = options['URI']
    activate(admin=True)
    app.run('0.0.0.0', debug=True)
