from django.db import models
from django.contrib.auth.models import User


class Article(models.Model):
    title = models.CharField(max_length=64, null=False, blank=False)
    author = models.ForeignKey(User, to_field="username", on_delete=models.CASCADE, null=False, blank=False)
    created = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    synopsis = models.CharField(max_length=312, null=False, blank=False)
    content = models.TextField(null=False, blank=False)

    def __str__(self):
        return self.title

class UserFavouriteArticle(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey("articles.Article", on_delete=models.CASCADE)

    def __str__(self):
        return self.article.title

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "article"], name="unique_favoris_by_user"),]
