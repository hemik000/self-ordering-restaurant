from rest_framework import routers
from django.urls import path, include
from . import views


urlpatterns = [
    path("", views.CustomerListView.as_view(), name="list_customer"),
    path("<str:token>", views.CustomerDetailView.as_view(), name="detail_user"),
    path("create/", views.CustomerCreateView.as_view(), name="create_customer",),
    # path("<str:pk>/edit", views.UserUpdateView.as_view(), name="update_user"),
    # path("<str:pk>/delete", views.UserDeleteView.as_view(), name="update_user"),
]
