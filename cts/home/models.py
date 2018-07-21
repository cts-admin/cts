from __future__ import absolute_import, unicode_literals

from django.db import models
from django.shortcuts import render

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core import blocks
from wagtail.admin.edit_handlers import StreamFieldPanel, FieldPanel

from .tasks import mail_task


class ContactPage(Page):
    intro = RichTextField(blank=True)
    thankyou_page_title = models.CharField(
        max_length=255, help_text="Title text to use for the 'thank you' page"
    )

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full"),
        FieldPanel('thankyou_page_title'),
    ]

    def serve(self, request, *args, **kwargs):
        from .forms import ContactForm

        if request.method == 'POST':
            form = ContactForm(request.POST)
            if form.is_valid():
                cts_mail = 'ctsadmin@conservationtechnologysolutions.org'
                name = form.cleaned_data['name']
                subject = form.cleaned_data['subject']
                sender = form.cleaned_data['sender']
                message = form.cleaned_data['message'] + '\n\nName: {}\nSender: {}'.format(name, sender)

                cc_myself = form.cleaned_data['cc_myself']

                recipients = [cts_mail]
                if cc_myself:
                    recipients.append(sender)
                mail_task.delay(subject, message, cts_mail, recipients)
                return render(request, 'home/thankyou.html', {
                    'page': self,
                    'name': name,
                })
        else:
            form = ContactForm()

        return render(request, 'home/contact_us.html', {
            'page': self,
            'form': form,
        })


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


class WBAHomePage(Page):
    body = RichTextField(null=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]

    subpage_types = ['blog.WBABlogIndexPage']

    template = 'home/wba_home_page.html'
