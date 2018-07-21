from __future__ import absolute_import, unicode_literals

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0', 'web', '.dev.conservationtechnologysolutions.org',
                 'www.dev.conservationtechnologysolutions.org', '104.131.38.9',
                 'wba.localhost']

EMAIL_SSL_KEYFILE = '/etc/letsencrypt/live/dev.conservationtechnologysolutions.org/privkey.pem'
EMAIL_SSL_CERTFILE = '/etc/letsencrypt/live/dev.conservationtechnologysolutions.org/fullchain.pem'

try:
    from .local import *
except ImportError:
    pass
