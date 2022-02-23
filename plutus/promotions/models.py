from django.db import models
from django.utils import timezone
from accounts.models import User
from brands.models import Brand
from ckeditor.fields import RichTextField

class Category(models.Model):

    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="categoriy_images")

    def __str__(self):
        return self.name


class PromotionType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Promotion(models.Model):
    
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True)
    promotion_type = models.ForeignKey(PromotionType, on_delete=models.SET_NULL, null=True)

    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="promotion_images")
    url = models.URLField()
    max_number = models.PositiveSmallIntegerField()
    close_at = models.DateTimeField()
    min_price = models.PositiveIntegerField(default=0)
    max_price = models.PositiveIntegerField(default=0)
    description = RichTextField(blank=True)

    PENDING = 0
    APPROVED = 1
    CLOSED = 2
    STATUS_CHOICES = (
        (PENDING, "รอคำอนุมัติ"),
        (APPROVED, "อนุมัติแล้ว"),
        (CLOSED, "ปิดแล้ว"),
    )

    

    status = models.IntegerField(choices=STATUS_CHOICES, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def is_closed(self):
        if self.status == self.CLOSED:
            return True
        
        if timezone.now() >= self.close_at:
            self.status = self.CLOSED
            self.save()
            return True

        return False
