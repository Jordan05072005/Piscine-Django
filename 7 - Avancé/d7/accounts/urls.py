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
from django.views.generic import CreateView
from .forms import LoginForm, SignUpForm
from django.urls import reverse_lazy, path
from django.contrib.auth.decorators import user_passes_test


urlpatterns = [
    path("login/", LoginView.as_view(
        form_class=LoginForm,
        template_name="login.html",
        next_page="articles",
    ), name="login"),
    path("register/", user_passes_test(
        lambda user: not user.is_authenticated,
        login_url="articles",
        redirect_field_name=None,
    )(CreateView.as_view(
        form_class=SignUpForm,
        template_name="signup.html",
        success_url=reverse_lazy("articles"),
    )), name="register"),
    path("logout/", LogoutView.as_view(next_page="articles"), name="logout"),
]
