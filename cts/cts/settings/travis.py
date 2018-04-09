from .base import *

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'testserver']
SECRET_KEY = 'This is a secret key for Travis CI'


DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.postgresql_psycopg2',
        'NAME':     'travis_ci_test',  # Must match travis.yml setting
        'USER':     'postgres',
        'PASSWORD': '',
        'HOST':     'localhost',
        'PORT':     '',
    }
}
