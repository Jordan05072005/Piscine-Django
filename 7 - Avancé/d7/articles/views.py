from .models import Article, UserFavouriteArticle
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView
from .forms import ArticleForm, FavoriteArticleForm
from django.contrib import messages
from django.shortcuts import redirect
from django.views import View
from django.urls import reverse



class PublishView(LoginRequiredMixin, CreateView):
    model = Article
    success_url = '/'
    template_name="article_create.html"
    form_class=ArticleForm
    modelCreate = UserFavouriteArticle

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class ArticleDetailView(DetailView):
    model=Article
    template_name="article_detail.html"
    context_object_name="article"
    pk_url_kwarg="id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = FavoriteArticleForm(initial={"article": self.object})
        context["favorite"] = (
            UserFavouriteArticle.objects.filter(user=self.request.user, article=self.object).first()
            if self.request.user.is_authenticated else None
        )
        return context


class AddFavouriteView(LoginRequiredMixin, CreateView):
    model = UserFavouriteArticle
    form_class = FavoriteArticleForm
    http_method_names = ["post"]
    
    def get_success_url(self):
        return reverse("article_detail", args=[self.object.article.id])

    def form_valid(self, form):
        article = form.cleaned_data["article"]
        if UserFavouriteArticle.objects.filter(user=self.request.user, article=article).exists():
            messages.info(self.request, "This item is already in your favorites.")
            return redirect("article_detail", id=article.id)
        form.instance.user = self.request.user
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Impossible d’ajouter cet article aux favoris.")
        article_id = self.request.POST.get("article")
        if article_id:
            return redirect("article_detail", id=article_id)
        return redirect("articles")
