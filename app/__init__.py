from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.mail import Mail
from flask.ext.bcrypt import Bcrypt
from flask_migrate import Migrate
import sys
import logging

app = Flask(__name__)


app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)

app.config.from_object('config')
mail = Mail(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

bcrypt = Bcrypt(app)

lm = LoginManager(app)
lm.login_view = 'login'
lm.init_app(app)

from app import models,views






