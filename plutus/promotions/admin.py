from django.contrib import admin
from promotions.models import Category, Promotion, PromotionType

class PromotionTypeAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]

class PromotionAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "status"]

admin.site.register(Category)
admin.site.register(PromotionType, PromotionTypeAdmin)
admin.site.register(Promotion, PromotionAdmin)

