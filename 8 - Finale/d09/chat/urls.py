"""
URL configuration for d09 project.

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
from django.views.generic import ListView
from django.urls import path
from .models import ChatRoom
from .views import RoomView

urlpatterns = [
    path('chatrooms/', ListView.as_view(
        model=ChatRoom,
        template_name='chatrooms.html',
        context_object_name='rooms'), name='chatrooms'),
    path('chatrooms/<str:room_name>/', RoomView.as_view(), name='chatroom'),]
