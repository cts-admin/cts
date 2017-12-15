from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.test import Client, TestCase

from .models import Profile


class ViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.credentials = {'username': 'a-user',
                           'password': 'password',
                           'email': 'email@email.com'}
        cls.user = User.objects.create_user(**cls.credentials)

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
