from django.urls import path
from promotions import views

app_name = "promotions"

urlpatterns = [
    path("", views.all_deals_view, name="all_deals"),
    path("flash", views.flash_deals_view, name="flash_deals"),
    path("categories/", views.category_list_view, name="category_list"),
    path("create_promotion/", views.create_promotion_view, name="create_promotion"),
    path("promotion_list_api/", views.promotion_list_apiview, name="promotion_list_api"),
    path("my_promotions/", views.my_promotion_list_view, name="my_promotion_list"),
    path("<int:pk>/", views.promotion_detail_view, name="promotion_detail"),
]
