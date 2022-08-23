from django.urls import path
from brands import views

app_name = "brands"

urlpatterns = [
    path("", views.brand_list_view, name="brand_list"),
    path("<int:pk>/", views.brand_feed_view, name="brand_feed"),
    path("<int:pk>/follow/", views.follow_brand_view, name="follow_brand"),
    path("<int:pk>/unfollow/", views.unfollow_brand_view, name="unfollow_brand"),
    path(
        "followed_brands/", views.followed_brand_list_view, name="followed_brand_list"
    ),
]
