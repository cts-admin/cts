from __future__ import absolute_import, unicode_literals

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'web', '0.0.0.0', '159.65.242.181']

EMAIL_SSL_KEYFILE = BASE_DIR + '/key.pem'
EMAIL_SSL_CERTFILE = BASE_DIR + '/certificate.pem'

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': os.environ.get('PG_DB', 'postgres'),
        'USER': os.environ.get('PG_USER', 'postgres'),
        'PASSWORD': os.environ['PG_PASSWORD'],
        'HOST': os.environ.get('DB_HOST', '0.0.0.0'),
        'PORT': '',
    }
}

try:
    from .local import *
except ImportError:
    pass
