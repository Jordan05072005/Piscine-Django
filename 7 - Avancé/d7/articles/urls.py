"""
URL configuration for d7 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from django.views.generic import ListView , DeleteView
from .models import Article
from .views import PublishView, ArticleDetailView, AddFavouriteView
from django.contrib.auth.decorators import login_required
from .models import UserFavouriteArticle

urlpatterns = [
    path("articles/", ListView.as_view(
        model=Article,
        template_name="articles.html",
        context_object_name="articles",
        # ordering=["-created"],
    ), name="articles"),
    path("articles/<int:id>/", ArticleDetailView.as_view(), name="article_detail"),
    path("articles/create/", login_required(PublishView.as_view()), name="publish"),
    path("favourites/add/", login_required(AddFavouriteView.as_view()), name="add_favourite"),
    path(
        "favourites/<int:pk>/delete/",
        login_required(DeleteView.as_view(
            model=UserFavouriteArticle,
            success_url="/articles/",
            http_method_names=["post"],
        )),
        name="delete_favorite",
    ),
]

