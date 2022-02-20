from django.db import models
from django.contrib.auth.models import User
from annoying.fields import AutoOneToOneField

class Profile(models.Model):
    MALE = 0
    FEMALE = 1

    GENDER_CHOICES = (
        (MALE, "ชาย"),
        (FEMALE, "หญิง"),
    )

    user = AutoOneToOneField(User, primary_key=True, on_delete=models.CASCADE)

    name = models.CharField(max_length=64)
    surname = models.CharField(max_length=64)
    email = models.EmailField(max_length=128)
    tel = models.CharField(max_length=15)
    information = models.TextField(blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    gender = models.IntegerField(choices=GENDER_CHOICES, default=MALE)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    image = models.ImageField(upload_to="profile_images", blank=True, null=True)

    def __str__(self):
        return f"{self.name} {self.surname}"
