from django.test import TestCase

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import translation
from pydoc import synopsis

from .models import Article,UserFavouriteArticle

class UnLoginAccessTests(TestCase):
    def setUp(self):
        translation.activate("en")

    def test_publish_access(self):
        response = self.client.get(reverse("publish"))
        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'article_create.html')


class LoginAccessTests(TestCase):
    def setUp(self):
        translation.activate("en")
        self.user = User.objects.create_user(username="bob", password="motdepasse123")
        self.client.force_login(self.user)


    def test_publish_access(self):
            response = self.client.get(reverse("publish"))
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'article_create.html')

class FavouritesTests(TestCase):
    def setUp(self):
        translation.activate("en")
        self.user = User.objects.create_user(username="bob", password="motdepasse123")
        self.client.force_login(self.user)
        Article.objects.create(title="title1", content="content1", synopsis="test", author=self.user)


    def test_double_favourite_same_article(self):
        article = Article.objects.get(title="title1")
        response = self.client.post(reverse("add_favourite"), {
            "article": article.id,
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            UserFavouriteArticle.objects.filter(user=self.user, article=article).count(),
            1,
        )
        response2 = self.client.post(reverse("add_favourite"), {"article": article.id})
        self.assertEqual(response2.status_code, 302)
        self.assertEqual(
            UserFavouriteArticle.objects.filter(user=self.user, article=article).count(),
            1,
        )




