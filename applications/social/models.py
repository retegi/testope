from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.

class TestChat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)
    text = models.TextField(max_length=100, null=True, blank=True)

    def __str__(self):
        return str(self.user)

