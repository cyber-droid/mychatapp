from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    public_key = models.TextField(null=True, blank=True)
    private_key = models.TextField(null=True, blank=True)

class ChatRoom(models.Model):
    name = models.CharField(max_length=100)
    is_public = models.BooleanField(default=True)

class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)  # Fixed typo here
    user = models.ForeignKey(User, on_delete=models.CASCADE)     # Fixed typo here
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)