from rest_framework import routers
from django.urls import path, include
from . import views


urlpatterns = [
    path("", views.OrderItemListView.as_view(), name="list_order_items"),
    # path("<str:pk>", views.UserDetailView.as_view(), name="detail_user"),
    path("create/", views.OrderItemCreateView.as_view(), name="create_order_items",),
    path(
        "<str:pk>/update/",
        views.OrderItemUpdateView.as_view(),
        name="update_order_item",
    ),
    # path("<str:pk>/delete", views.UserDeleteView.as_view(), name="update_user"),
]
