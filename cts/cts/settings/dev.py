from __future__ import absolute_import, unicode_literals

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1']

EMAIL_SSL_KEYFILE = '/home/ave/PycharmProjects/cts/privkey.pem'
EMAIL_SSL_CERTFILE = '/home/ave/PycharmProjects/cts/fullchain.pem'

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': os.environ['DJANGO_DB_PASS'],
        'HOST': '0.0.0.0',
        'PORT': '',
    }
}

try:
    from .local import *
except ImportError:
    pass
