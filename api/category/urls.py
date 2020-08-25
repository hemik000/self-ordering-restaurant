from rest_framework import routers
from django.urls import path, include
from . import views


urlpatterns = [
    path("", views.ListCategory.as_view(), name="list_category"),
]
