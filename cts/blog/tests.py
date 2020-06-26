import pytest

from django.core.management import call_command
from wagtail.core.models import Page


@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        welcome = Page.objects.get(title="Welcome to your new Wagtail site!")
        welcome.delete()
        call_command('loaddata', 'blog_test_fixtures.json')


def test_blog_page(django_db_setup, db, client):
    response = client.get('/cts-blog/')
    assert response.status_code == 200
