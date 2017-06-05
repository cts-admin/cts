from __future__ import absolute_import, unicode_literals

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '***REMOVED***'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp-relay.gmail.com'
EMAIL_PORT = 25
EMAIL_HOST_USER = 'ctsadmin@conservationtechnologysolutions.com'
EMAIL_HOST_PASSWORD = '***REMOVED***'
EMAIL_USE_TLS = False
EMAIL_USE_SSL = False
#EMAIL_SSL_KEYFILE = '/home/ave/PycharmProjects/cts/privkey.pem'
#EMAIL_SSL_CERTFILE = '/home/ave/PycharmProjects/cts/cert.pem'
EMAIL_TIMEOUT = 10

DEFAULT_FROM_EMAIL = 'ctsadmin@conservationtechnologysolutions.com'
SERVER_EMAIL = 'ctsadmin@conservationtechnologysolutions.com'
ADMINS = [('Avery', 'ctsadmin@conservationtechnologysolutions.com')]



try:
    from .local import *
except ImportError:
    pass
