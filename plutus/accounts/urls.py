from django.urls import path
from accounts import views

app_name = "accounts"

urlpatterns = [
    path("logout/", views.logout_view, name="logout"),
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("profile/", views.profile_view, name="profile"),
    path("change_password/", views.change_password_view, name="change_password"),
]
