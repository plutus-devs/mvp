from django.contrib import admin
from notifications.models import Notification

class NotificationAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "message", "url", "created_at")

admin.site.register(Notification, NotificationAdmin)
