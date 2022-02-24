from django.urls import path
from orders import views

app_name = "orders"

urlpatterns = [
    path("create/<int:promotion_pk>/", views.create_order_view, name="create_order"),
    path("<int:pk>/", views.order_detail_view, name="order_detail"),
    path("<int:pk>/upload_deposit/", views.upload_deposit_view, name="upload_deposit"),
    path("<int:pk>/upload_full/", views.upload_full_view, name="upload_full"),
]