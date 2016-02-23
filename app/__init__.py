from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.mail import Mail
from flask.ext.moment import Moment
from flask.ext.bcrypt import Bcrypt
from flask_migrate import Migrate



app = Flask(__name__)

app.config.from_object('config')
mail = Mail(app)
moment = Moment(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

bcrypt = Bcrypt(app)

lm = LoginManager(app)
lm.login_view = 'login'
lm.init_app(app)

from app import models,views






