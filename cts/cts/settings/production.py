from __future__ import absolute_import, unicode_literals

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['.conservationtechnologysolutions.com', '104.236.198.4', '165.227.186.154']

EMAIL_SSL_KEYFILE = '/etc/letsencrypt/live/conservationtechnologysolutions.com/privkey.pem'
EMAIL_SSL_CERTFILE = '/etc/letsencrypt/live/conservationtechnologysolutions.com/fullchain.pem'

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

try:
    from .local import *
except ImportError:
    pass
