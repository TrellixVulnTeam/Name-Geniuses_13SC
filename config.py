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

OAUTH_CREDENTIALS = {
    'facebook': {
        'id': '1027820050615086',
        'secret': 'f6ef9bb473fd20dabc2bfa897cf3b2f9'
    },
    'google': {
            'id': '1025055206557-t3t0gb3ljfbtbhpp2k364c2egia06tht.apps.googleusercontent.com',
            'secret':'_LIus0fWYyarUbQrH9oFu1H4'
    }
 
}

# mail server settings
# email server
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = 'dalecudmore@gmail.com'
MAIL_PASSWORD='Seal1951'

# administrator list
ADMINS = ['dalecudmore@gmail.com']

# pagination
POSTS_PER_PAGE = 3

SQLALCHEMY_RECORD_QUERIES = True
# slow database query threshold (in seconds)
DATABASE_QUERY_TIMEOUT = 0.5

BCRYPT_LOG_ROUNDS = 12
SECURITY_PASSWORD_SALT = 'my_precious_two'