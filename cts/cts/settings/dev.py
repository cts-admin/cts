from __future__ import absolute_import, unicode_literals

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

EMAIL_SSL_KEYFILE = '/home/ave/PycharmProjects/cts/privkey.pem'
EMAIL_SSL_CERTFILE = '/home/ave/PycharmProjects/cts/fullchain.pem'

try:
    from .local import *
except ImportError:
    pass
