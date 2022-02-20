from django.contrib import admin
from accounts.models import Profile
from django.contrib.auth.models import User, Group

class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user",)

admin.site.unregister(Group)
admin.site.register(Profile, ProfileAdmin)
