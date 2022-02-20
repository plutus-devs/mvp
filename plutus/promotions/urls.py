from django.urls import path
from promotions import views

app_name = "promotions"

urlpatterns = [
    path("", views.all_deals_view, name="all_deals"),
]