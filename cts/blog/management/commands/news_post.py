from datetime import datetime

from django.core.management.base import BaseCommand
from blog.models import BlogCategory, BlogIndexPage, BlogPage

news_cat = BlogCategory.objects.get(name='News')
index_page = BlogIndexPage.objects.get(title="CTS Blog").specific


class Command(BaseCommand):
    help = 'Blog post mechanism to get conservation news.'

    def get_data(self):
        data = {}
        return data

    def _create_post(self):
        data = self.get_data()
        date_str = datetime.now().date().strftime('%m-%d-%Y')
        title = "Conservation News: " + date_str
        news_post = BlogPage(
            title=title,
            slug='news-' + date_str,
            date=datetime.now(),
            intro=data['intro'],
            body=data['body'],
            categories=[news_cat],
        )
        index_page.add_child(instance=news_post)

    def handle(self, *args, **options):
        self._create_post()

