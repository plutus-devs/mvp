from django.db import models
from django.urls import reverse
from django.utils import timezone
from promotions.models import Promotion
from accounts.models import User
from notifications.models import Notification

class Order(models.Model):
    promotion = models.ForeignKey(Promotion, null=True, blank=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)

    product_id = models.CharField(max_length=255)
    full_price = models.FloatField()
    description = models.TextField(blank=True)
    product_name = models.CharField(max_length=255, blank="", default="")
 
    discount_price = models.FloatField(default=0)
    deposit = models.FloatField(default=0)
    dept = models.FloatField(default=0)

    deposit_image = models.ImageField(upload_to="order_images", blank=True, null=True)
    full_image = models.ImageField(upload_to="order_images", blank=True, null=True)

    PENDING = 0
    REJECTED = 1
    APPROVED = 2
    DEPOSIT_PAID = 3
    COMPLETED = 7

    STATUS_CHOICES = (
        (PENDING, "รออนุมัติ"),
        (REJECTED,"ถูกปฏิเสธ"),
        (APPROVED,"อนุมัติแล้ว กรุณาชำระมัดจำ"),
        (DEPOSIT_PAID,"จ่ายมันจำเรียบร้อยแล้ว กรุณาชำระค่าบริการทั้งหมด"),
        (4,"ร้านค้าส่งสินค้ามา PLUTUS"),
        (5,"PLUTUS กำลังแยกสินค้า"),
        (6,"ออกจาก PLUTUS แล้ว"),
        (COMPLETED,"เรียบร้อยแล้ว"),
    )

    status = models.IntegerField(choices=STATUS_CHOICES, default=0)

    status0 = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    status1 = models.DateTimeField(blank=True, null=True)
    status2 = models.DateTimeField(blank=True, null=True)
    status3 = models.DateTimeField(blank=True, null=True)
    status4 = models.DateTimeField(blank=True, null=True)
    status5 = models.DateTimeField(blank=True, null=True)
    status6 = models.DateTimeField(blank=True, null=True)
    status7 = models.DateTimeField(blank=True, null=True)
    status8 = models.DateTimeField(blank=True, null=True)

    def get_timeline(self, sid):
        status_field = f"status{sid}"
        timestamp = getattr(self, status_field, None)
        text = None
        for v, t in self.STATUS_CHOICES:
            if v == sid:
                text = t
        
        return {
            "text": text,
            "active": timestamp is not None,
            "timestamp": "" if timestamp is None else timestamp.strftime("%b. %d, %H:%M")
        }

    def save(self, *args, **kwargs):
        status_field = f"status{self.status}"
        for i in range(self.status+1, 12):
            setattr(self, f"status{i}", None)
        for i in range(0, self.status+1):
            if getattr(self, f"status{i}", None) is None:
                setattr(self, f"status{i}", timezone.now())

        noti = Notification(
            user=self.user,
            title=f"{self.product_id} - {self.promotion.name}",
            message="คำสั่งซื้อของคุณมีอัพเดท",
            url=reverse("orders:order_detail", kwargs={"pk": self.id}),
        )
        noti.save()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"Order-{self.id}"