from __future__ import absolute_import, unicode_literals

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'testserver', '0.0.0.0']

EMAIL_SSL_KEYFILE = '/home/ave/PycharmProjects/cts/privkey.pem'
EMAIL_SSL_CERTFILE = '/home/ave/PycharmProjects/cts/fullchain.pem'

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': os.environ.get('PG_DB', 'postgres'),
        'USER': os.environ.get('PG_USER', 'postgres'),
        'PASSWORD': os.environ['DJANGO_DB_PASS'],
        'HOST': os.environ.get('DOCKER_HOST', '0.0.0.0'),
        'PORT': '',
    }
}

try:
    from .local import *
except ImportError:
    pass
