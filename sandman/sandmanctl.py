"""Script to run sandman via command line."""
from __future__ import absolute_import

import click

from sandman import app
from sandman.model import activate

def print_version(ctx, value):
    """Print the current version of sandman and exit."""
    if not value:
        return
    import pkg_resources
    version = None
    try:
        version = pkg_resources.get_distribution('sandman').version
    finally:
        del pkg_resources
    click.echo(version)
    ctx.exit()


@click.command()
@click.option('--generate-pks/--no-generate-pks', default=False,
        help='Have sandman generate primary keys for tables without one')
@click.option('--show-pks/--no-show-pks', default=False,
        help='Have sandman show primary key columns in the admin view')
@click.option('--host', default='0.0.0.0',
        help='Hostname sandman should bind to')
@click.option('--port', default=8080,
        help='Port sandman should bind to')
@click.option('--version', is_flag=True,
        callback=print_version, expose_value=False, is_eager=True)
@click.argument('URI', metavar='<URI>')
def run(generate_pks, show_pks, host, port, uri):
    """Connect sandman to <URI> and start the API server/admin
    interface."""
    app.config['SQLALCHEMY_DATABASE_URI'] = uri
    app.config['SANDMAN_GENERATE_PKS'] = generate_pks
    app.config['SANDMAN_SHOW_PKS'] = show_pks
    app.config['SERVER_HOST'] = host
    app.config['SERVER_PORT'] = port
    activate(name='sandmanctl')
    app.run(host=host, port=int(port), debug=True)
