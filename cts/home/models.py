from __future__ import absolute_import, unicode_literals

from django.db import models

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore import blocks
from wagtail.wagtailadmin.edit_handlers import StreamFieldPanel, FieldPanel


class HomePage(Page):
    body = StreamField([
        ('motto', blocks.CharBlock()),
        ('paragraph', blocks.RichTextBlock())
    ], blank=True)
    use_detail_template = models.BooleanField()

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
        FieldPanel('use_detail_template')
    ]

    def get_template(self, request, *args, **kwargs):
        if self.use_detail_template:
            return 'home/mission.html'
        return 'home/home_page.html'
