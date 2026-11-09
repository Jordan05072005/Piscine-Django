from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from django.conf import settings
from .models import ChatRoom, ChatMessage


class RoomView(LoginRequiredMixin, TemplateView):
    template_name = 'chatroom.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = self.kwargs['room_name']
        context['system_username'] = settings.DATA_ENV["SYSTEM_USERNAME"]
        return context