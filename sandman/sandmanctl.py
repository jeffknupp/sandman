"""Script to run sandman via command line

Usage:
    sandmanctl.py URI [--show-pks --generate-pks] [--host=host] [--port=port] [--version]
    sandmanctl.py --version

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
    -h --help                   Show this screen.
    -s --show-primary-keys      Display primary key columns in the admin
                                interface
    -g --generate-pks           Use the combination of all columns as the
                                primary key for tables without primary keys
                                (primary keys are required by the mapping
                                engine). Implies --primary-keys
    -v --version                Display current version of sandman and exit
    --host <host>               Host to run sandmanctl on
    --port <port>               Port to run sandmanctl on

'postgresql+psycopg2://scott:tiger@localhost/test'
'postgresql+psycopg2://scott:tiger@localhost/test' --generate-pks --host localhost --port 8080
'sqlite+pysqlite:///relative/path/to/db.db'
'sqlite:////absolute/path/to/db.db'

"""
from __future__ import absolute_import
import sys

from docopt import docopt

from sandman import app
from sandman.model import activate

def main(test_options=None):
    """Main entry point for script."""
    import pkg_resources
    version = None
    try:
        version = pkg_resources.get_distribution('sandman').version
    finally:
        del pkg_resources

    options = test_options or docopt(__doc__, version=version)
    URI = options['URI']
    app.config['SQLALCHEMY_DATABASE_URI'] = options['URI']
    app.config['SANDMAN_GENERATE_PKS'] = options['--generate-pks'] or False
    app.config['SANDMAN_SHOW_PKS'] = options['--show-pks'] or False
    host = options.get('--host') or '0.0.0.0'
    port = options.get('--port') or 5000
    app.config['SERVER_HOST'] = host
    app.config['SERVER_PORT'] = port
    activate(name='sandmanctl')
    app.run(host=host, port=int(port), debug=True)
