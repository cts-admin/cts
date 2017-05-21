from __future__ import absolute_import, unicode_literals

from django.db import models

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore import blocks
from wagtail.wagtailadmin.edit_handlers import StreamFieldPanel


class HomePage(Page):
    content = StreamField([
        ('heading', blocks.CharBlock(classname='text-center')),
        ('motto', blocks.CharBlock(classname='subtitle')),
        ('paragraph', blocks.RichTextBlock())
    ], blank=True)

    content_panels = Page.content_panels + [
        StreamFieldPanel('content', classname='full'),
    ]
