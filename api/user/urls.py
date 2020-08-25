from rest_framework import routers
from django.urls import path, include
from . import views


urlpatterns = [
    path("", views.UserListView.as_view(), name="list_user"),
    path("<str:pk>", views.UserDetailView.as_view(), name="detail_user"),
    path("create/", views.UserCreateView.as_view(), name="create_user"),
    path("<str:pk>/edit", views.UserUpdateView.as_view(), name="update_user"),
    path("<str:pk>/delete", views.UserDeleteView.as_view(), name="update_user"),
]


# from .views import UserViewSet
# from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register(r"", UserViewSet, basename="user")
# urlpatterns = router.urls
