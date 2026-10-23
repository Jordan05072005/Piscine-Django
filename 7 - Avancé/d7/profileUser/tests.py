from django.test import TestCase

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import translation

class UnLoginAccessTests(TestCase):

    def test_favourites_access(self):
        response = self.client.get(reverse("profileFavourites"))
        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'profile_favourites_page.html')


    def test_publication_access(self):
        response = self.client.get(reverse("profileArticles"))
        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'profile_articles.html')

class LoginAccessTests(TestCase):

    def setUp(self):
        translation.activate("en")
        self.user = User.objects.create_user(username="bob", password="motdepasse123")
        self.client.force_login(self.user)

    def test_favourites_access(self):
        response = self.client.get(reverse("profileFavourites"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile_favourites_page.html')

    def test_publication_access(self):
        response = self.client.get(reverse("profileArticles"))
        self.assertEqual(response.status_code, 200  )
        self.assertTemplateUsed(response, 'profile_articles.html')



