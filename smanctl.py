from sandman import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://nathan:password@localhost:5432/nathan'

from sandman.model import activate

activate()

app.run()

