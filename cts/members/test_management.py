
from datetime import date, timedelta

from django.conf import settings
from django.core import mail
from django.core.management import call_command
from django.test import TestCase
from django.utils.formats import localize

from .models import SILVER_MEMBERSHIP, CorporateMember


class CorporateMemberTests(TestCase):
    today = date.today()
    twenty_nine_days_from_now = today + timedelta(days=29)
    thirty_days_from_now = today + timedelta(days=30)

    @classmethod
    def setUpTestData(cls):
        cls.member = CorporateMember.objects.create(
            display_name='Corporation',
            billing_name='foo',
            billing_email='billing@example.com',
            contact_email='contact@example.com',
            contact_name='Contact Name',
            membership_level=SILVER_MEMBERSHIP,
        )

    def test_no_email(self):
        self.member.invoice_set.create(amount=0, expiration_date=self.twenty_nine_days_from_now)
        call_command('send_renewal_emails')
        self.assertEqual(len(mail.outbox), 0)

    def test_mail(self):
        self.member.invoice_set.create(amount=0, expiration_date=self.thirty_days_from_now)
        call_command('send_renewal_emails')
        self.assertEqual(len(mail.outbox), 1)
        msg = mail.outbox.pop()
        self.assertEqual(msg.subject, 'Expiring Conservation Technology Solutions Membership for Corporation')
        self.assertIn('Hi Contact Name,', msg.body)
        self.assertIn(
            'The Conservation Technology Solutions membership for Corporation expires\n'
            '%s. Would you like to renew your support?' % localize(self.thirty_days_from_now),
            msg.body
        )
        self.assertIn('http://127.0.0.1:8000/foundation/corporate-membership/renew/', msg.body)
        self.assertEqual(msg.from_email, settings.DEFAULT_FROM_EMAIL)
        self.assertEqual(
            msg.to,
            [
                settings.DEFAULT_FROM_EMAIL,
                'info@conservationtechnologysolutions.com',
                'ctsadmin@conservationtechnologysolutions.com',
            ]
        )
