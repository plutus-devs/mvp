from django.contrib import admin
from .models import Order


class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id", "promotion", "product_name", "user", "full_price", "discount_price",
    )


admin.site.register(Order, OrderAdmin)
