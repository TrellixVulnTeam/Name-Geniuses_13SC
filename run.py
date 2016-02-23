#!flask/bin/python
from app import app
#app.run(host='0.0.0.0', port=5000, debug=True)
from flask.ext.script import Manager
from flask.ext.migrate import MigrateCommand

manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()