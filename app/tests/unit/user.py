from django.contrib.auth.models import User
from django.contrib.auth import get_user
from django.test import TestCase


class CreateUserTests(TestCase):


    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create(username='user1', password='pswd1')

    def test_get(self):
        response = self.client.get('/create_user')
        self.assertEquals(1, len(User.objects.all()))
        self.assertFalse(response.context['form'].errors)
        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)

    def test_post_valid_user_info(self):
        self.client.post('/create_user', {'username': 'user1234', 'password1': 'skdj345%kjdf', 'password2': 'skdj345%kjdf'})
        self.assertEquals(2, len(User.objects.all()))
        user = get_user(self.client)
        self.assertEquals('user1234', user.username)
        self.assertTrue(user.is_authenticated)

    def test_post_invalid_passwords(self):
        self.client.post('/create_user', {'username': 'user1234', 'password1': 'skdj345%kjdf', 'password2': 'different123'})
        self.assertEquals(1, len(User.objects.all()))
        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)

    def test_post_existing_user(self):
        self.client.post('/create_user', {'username': 'user1', 'password1': 'skdj345%kjdf', 'password2': 'skdj345%kjdf'})
        self.assertEquals(1, len(User.objects.all()))
        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)

