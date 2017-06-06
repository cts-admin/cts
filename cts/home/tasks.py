from __future__ import absolute_import, unicode_literals
from celery import shared_task

from django.core.mail import send_mail


@shared_task
def mail_task(subject, message, mail_from, mail_to):
    send_mail(subject, message, mail_from, mail_to)
