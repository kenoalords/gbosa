from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=128)
    link = models.CharField(max_length=512, null=True, blank=True)
    is_viewed = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=datetime.now)
