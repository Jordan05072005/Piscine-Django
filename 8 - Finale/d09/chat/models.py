from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class ChatRoom(models.Model):
    name = models.CharField(max_length=200)
    users = models.ManyToManyField(User)

class ChatMessage(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

