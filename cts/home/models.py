***REMOVED***

from django.core.mail import send_mail
from django.db import models
from django.shortcuts import render

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailcore import blocks
from wagtail.wagtailadmin.edit_handlers import StreamFieldPanel, FieldPanel


class ContactPage(Page):
    intro = RichTextField(blank=True)
    thankyou_page_title = models.CharField(
        max_length=255, help_text="Title text to use for the 'thank you' page"
    )

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full"),
        FieldPanel('thankyou_page_title'),
    ***REMOVED***

    def serve(self, request):
        from .forms import ContactForm

        if request.method == 'POST':
            form = ContactForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data['name'***REMOVED***
                subject = form.cleaned_data['subject'***REMOVED***
                message = form.cleaned_data['message'***REMOVED***
                sender = form.cleaned_data['sender'***REMOVED***
                cc_myself = form.cleaned_data['cc_myself'***REMOVED***

                recipients = ['ctsadmin@conservationtechnologysolutions.com'***REMOVED***
                if cc_myself:
                    recipients.append(sender)
                send_mail(subject, message, sender, recipients)
                return render(request, 'home/thankyou.html', {
                    'page': self,
                    'name': name,
            ***REMOVED***)
        else:
            form = ContactForm()

        return render(request, 'home/contact_us.html', {
            'page': self,
            'form': form,
    ***REMOVED***)


class HomePage(Page):
    body = StreamField([
        ('motto', blocks.CharBlock()),
        ('paragraph', blocks.RichTextBlock())
    ***REMOVED***, blank=True)
    use_detail_template = models.BooleanField()

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
        FieldPanel('use_detail_template')
    ***REMOVED***

    def get_template(self, request, *args, **kwargs):
        if self.use_detail_template:
            return 'home/mission.html'
        return 'home/home_page.html'
