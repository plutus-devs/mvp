from django.db import models
from accounts.models import User


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    title = models.CharField(max_length=255)
    message = models.TextField()
    url = models.URLField()

    read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
