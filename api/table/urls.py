from rest_framework import routers
from django.urls import path, include
from . import views


urlpatterns = [
    path("", views.TableListView.as_view(), name="list_table"),
    path("<str:pk>", views.TableDetailView.as_view(), name="retrive_table"),
]
