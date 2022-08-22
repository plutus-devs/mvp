from django.contrib import admin
from brands.models import Brand, BrandImage


class BrandImageInline(admin.TabularInline):
    model = BrandImage
    extra = 1


class BrandAdmin(admin.ModelAdmin):
    list_display = ("id", "name",)
    inlines = [BrandImageInline]


admin.site.register(Brand, BrandAdmin)
