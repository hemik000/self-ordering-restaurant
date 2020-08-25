from rest_framework import routers
from django.urls import path, include
from . import views


urlpatterns = [
    path("", views.MenuListView.as_view(), name="list_menu"),
    # path("<str:pk>", views.UserDetailView.as_view(), name="detail_user"),
    # path("create/", views.CustomerCreateView.as_view(), name="create_customer",),
    # path("<str:pk>/create/menu", views.OrderCreateView.as_view(), name="update_order"),
    # path("<str:pk>/delete", views.UserDeleteView.as_view(), name="update_user"),
]
