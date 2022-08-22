from django.db import models
from accounts.models import User


class Brand(models.Model):
    users = models.ManyToManyField(User, blank=True)
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class BrandImage(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="brand_images")
