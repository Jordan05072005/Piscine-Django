from django.test import TestCase

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import translation

class UnLoginAccessTests(TestCase):
    def setUp(self):
        translation.activate("en")

    def test_register_access(self):
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')


class LoginAccessTests(TestCase):
    def setUp(self):
        translation.activate("en")
        self.user = User.objects.create_user(username="bob", password="motdepasse123")
        self.client.force_login(self.user)


    def test_register_access(self):
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'signup.html')



