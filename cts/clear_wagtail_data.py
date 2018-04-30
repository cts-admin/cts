import cts.wsgi

from wagtail.core.models import Page


default_page = Page.objects.get(title='Welcome to your new Wagtail site!')
default_page.delete()
