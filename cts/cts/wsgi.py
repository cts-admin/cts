***REMOVED***
WSGI config for cts project.

It exposes the WSGI callable as a module-level variable named ``application``.

***REMOVED***
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
***REMOVED***

***REMOVED***

***REMOVED***

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cts.settings.dev")

application = get_wsgi_application()
