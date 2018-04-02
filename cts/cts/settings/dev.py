from __future__ import absolute_import, unicode_literals

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'web', '0.0.0.0', '.dev.conservationtechnologysolutions.com',
                 'www.dev.conservationtechnologysolutions.com', '165.227.186.154']

EMAIL_SSL_KEYFILE = '/etc/letsencrypt/live/dev.conservationtechnologysolutions.com/privkey.pem'
EMAIL_SSL_CERTFILE = '/etc/letsencrypt/live/dev.conservationtechnologysolutions.com/fullchain.pem'

try:
    from .local import *
except ImportError:
    pass
