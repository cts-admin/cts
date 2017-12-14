import datetime

from django.conf import settings
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string

from ...models import CorporateMember
from home.tasks import mail_task


class Command(BaseCommand):

    def handle(self, *args, **options):
        thirty_days_from_now = datetime.date.today() + datetime.timedelta(days=30)
        for member in CorporateMember.objects.filter(inactive=False):
            if member.get_expiry_date() == thirty_days_from_now:
                mail_task(
                    'Expiring Conservation Technology Solutions Membership for %s' % member.display_name,
                    render_to_string('members/corporate_member_renewal_email.txt', {
                        'contact_name': member.contact_name,
                        'member_name': member.display_name,
                        'expiry_date': member.get_expiry_date(),
                        'renewal_link': member.get_renewal_link(),
                    }),
                    settings.DEFAULT_FROM_EMAIL,
                    [
                        settings.DEFAULT_FROM_EMAIL,
                        member.contact_email,
                        'ctsadmin@conservationtechnologysolutions.com'
                    ],
                    )
