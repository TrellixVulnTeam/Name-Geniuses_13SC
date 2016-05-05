# -*- coding: utf-8 -*-
WTF_CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

    
import os
basedir = os.path.abspath(os.path.dirname(__file__))

if os.environ.get('DATABASE_URL') is None:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_RECORD_QUERIES = True

# mail server settings
# email server
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = 'dalecudmore@gmail.com'
MAIL_PASSWORD='Seal1951'

# administrator list
ADMINS = ['dale@namegeniuses.com']


SQLALCHEMY_RECORD_QUERIES = True
# slow database query threshold (in seconds)
DATABASE_QUERY_TIMEOUT = 0.5

BCRYPT_LOG_ROUNDS = 12
SECURITY_PASSWORD_SALT = 'my_precious_two'