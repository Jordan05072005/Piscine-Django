from django import forms
from .models import Article, UserFavouriteArticle

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["title", "synopsis", "content"]

class FavoriteArticleForm(forms.ModelForm):
    class Meta:
        model = UserFavouriteArticle
        fields = ["article"]
