import cts.wsgi

from django.db.utils import ProgrammingError
from wagtail.core.models import Page


try:
    default_page = Page.objects.get(title='Welcome to your new Wagtail site!')
    default_page.delete()
except ProgrammingError:
    print("Wagtail welcome page already deleted!")
