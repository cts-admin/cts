import re

from django.contrib.auth import get_user_model
from django.core import mail
from django.shortcuts import reverse
from django.test import Client, TestCase

from .models import Profile

User = get_user_model()


class ViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.credentials = {'username': 'a-user',
                           'password': 'password',
                           'email': 'email@email.com'}
        cls.user = User.objects.create_user(**cls.credentials)

    def test_admin_to_profile(self):
        """
        Logging in via wagtail admin and then attempting to visit
        the edit profile page would produce various errors since
        it circumvented the expected process logging in via the
        CTS login page.
        """
        err_c = Client()
        admin_creds = {'username': 'admin',
                       'password': 'password',
                       'email': 'admin@email.com'}
        User.objects.create_superuser(**admin_creds)
        admin_login_response = self.client.post(reverse('wagtailadmin_login'),
                                                {'username': 'admin', 'password': 'password'},
                                                follow=True)
        admin_fail_response = err_c.post(reverse('wagtailadmin_login'),
                                         {'username': 'admin', 'password': 'wrong'},
                                         follow=True)
        self.assertTrue(admin_login_response.context['user'].is_authenticated)
        self.assertFalse(admin_fail_response.context['user'].is_authenticated)

        profile_response = self.client.get(reverse('edit_profile'), follow=True)
        profile_fail_response = err_c.get(reverse('edit_profile'), follow=True)
        self.assertContains(profile_response, "Edit Your Profile")
        self.assertNotContains(profile_fail_response, "Edit Your Profile")

    def test_user_profile(self):
        self.assertEqual(User.objects.count(), 1)
        self.client.login(username='a-user', password='password')
        # Profile model does not exist until attempting to access edit profile view
        edit_response = self.client.get(reverse('edit_profile'))
        self.assertContains(edit_response, 'a-user')
        self.assertContains(edit_response, 'Edit Your Profile')
        self.assertEqual(Profile.objects.count(), 1)
        response = self.client.get(reverse('user_profile', args=['a-user']))
        self.assertContains(response, 'a-user')
        self.assertContains(response, 'User Profile')

    def test_login_redirect(self):
        response = self.client.post(reverse('login'), {
            'username': 'a-user',
            'password': 'password'
        })
        self.assertRedirects(response, reverse('edit_profile'))

    def test_profile_view_reversal(self):
        """
        The profile view can be reversed for usernames containing "weird" but
        valid username characters.
        """
        for username in ['asdf', '@asdf', 'asd-f', 'as.df', 'as+df']:
            reverse('user_profile', args=[username])

    def test_user_registration_user(self):
        """
        Test the registration workflow creates an inactive user, but not when
        an existing email address is used.
        """
        c = Client()
        # Should create a new user
        success_reg_response = c.post(reverse('django_registration_register'),
                                      {'username': 'another_user',
                                       'email': 'another_user@email.com',
                                       'password1': 'secret',
                                       'password2': 'secret'}, follow=True)
        print(success_reg_response.content)
        self.assertContains(success_reg_response,
                            'An activation link has been sent to the email address you supplied,'
                            ' along with instructions for activating your account.')
        self.assertTrue(User.objects.filter(username='another_user').exists())
        self.assertFalse(User.objects.get(username='another_user').is_active)

        # Should not create a new user
        fail_reg_response = c.post(reverse('django_registration_register'),
                                   {'username': 'diff_user_same_email',
                                    'email': 'another_user@email.com',
                                    'password1': 'secret',
                                    'password2': 'secret'}, follow=True)
        self.assertContains(fail_reg_response, 'This email address is already in use. Please supply a '
                                                       'different email address.')
        self.assertFalse(User.objects.filter(username='diff_user_same_email').exists())

    def test_user_registration_email(self):
        """
        Test the registration workflow creates an inactive user
        """
        c = Client()
        # Should create a new user
        c.post(reverse('django_registration_register'),
               {'username': 'another_user',
                'email': 'another_user@email.com',
                'password1': 'secret',
                'password2': 'secret'}, follow=True)
        # Test that one message has been sent.
        self.assertEqual(len(mail.outbox), 1)
        # Verify that the subject of the first message is correct.
        self.assertEqual(mail.outbox[0].subject, 'Activate your CTS account')
        email_body = mail.outbox[0].body
        activation_link = re.findall("(?P<activation_link>http\S+accounts/activate\S+)",
                                     email_body)[0]
        activation_response = c.get(activation_link, follow=True)
        self.assertContains(activation_response, 'Thanks for signing up! Now you can')
