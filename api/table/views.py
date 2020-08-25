from rest_framework.generics import ListAPIView, RetrieveAPIView
from .models import Table
from .serializers import TableSerializer
from rest_framework.permissions import AllowAny


class TableListView(ListAPIView):
    queryset = Table.objects.all()
    serializer_class = TableSerializer
    permission_classes = [AllowAny]

class TableDetailView(RetrieveAPIView):
    queryset = Table.objects.all()
    serializer_class = TableSerializer
    permission_classes = [AllowAny]
