"""Run server"""
from sandman.application import get_app
app = get_app('test', 'sqlite+pysqlite:///tests/data/existing.sqlite3')
import models
app.run(host='0.0.0.0', debug=True)
