from .serializers import MenuSerializer
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from .models import Menu
from django_filters.rest_framework import DjangoFilterBackend


class MenuListView(ListAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [
        AllowAny,
    ]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["category", "type"]
