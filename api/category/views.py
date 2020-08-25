from .serializers import CategorySerializer
from rest_framework.generics import ListAPIView, ListCreateAPIView
from .models import Category
from rest_framework.permissions import AllowAny

# Create your views here.


class ListCategory(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
