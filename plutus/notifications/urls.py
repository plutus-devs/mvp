from django.urls import path
from notifications import views


app_name = "notifications"

urlpatterns = [
    path("get_notifications/", views.notification_list_apiview, name="notification_list_api"),
    path("read_notification/<int:pk>", views.read_notification_view, name="read_notification"),
]