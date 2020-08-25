from rest_framework import status
from rest_framework.response import Response
from api.customer.serializers import CreatCustomerSerializer, DetailCustomerSerializer
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
    CreateAPIView,
)
from rest_framework.permissions import (
    AllowAny,
    IsAdminUser,
    IsAuthenticated,
)
from .models import Customer


# def is_session_valid(token, id):
#     print(id)
#     return True


class CustomerCreateView(CreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CreatCustomerSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class CustomerListView(ListAPIView):
    queryset = Customer.objects.all()
    serializer_class = CreatCustomerSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class CustomerDetailView(RetrieveAPIView):
    queryset = Customer.objects.all()
    serializer_class = DetailCustomerSerializer
    lookup_field = "token"
