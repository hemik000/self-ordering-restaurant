from api.order.permissions import IsSessionActive
from rest_framework import permissions
from api.order.models import Order
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    DestroyAPIView,
    UpdateAPIView,
)
from .models import OrderItem
from .serializers import (
    OrderItemCreateSerializers,
    OrderItemSerializers,
    OrderItemUpdateSerializers,
)
from rest_framework.exceptions import NotFound
from rest_framework import filters


class OrderItemListView(ListAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializers
    permission_classes = [
        IsSessionActive,
    ]
    filter_backends = [filters.OrderingFilter]
    ordering = ["quantity"]

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        customer = self.request.customer
        try:
            order = Order.objects.get(customer=customer)
        except Order.DoesNotExist:
            # from django.http import Http404
            raise NotFound("Order item empty")

        return OrderItem.objects.filter(order=order)


class OrderItemUpdateView(UpdateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemUpdateSerializers
    permission_classes = [
        IsSessionActive,
    ]


class OrderItemCreateView(CreateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemCreateSerializers
    permission_classes = [
        IsSessionActive,
    ]

    def perform_create(self, serializer):
        customer = self.request.customer
        order = Order.objects.get(customer=customer)
        serializer.save(order=order)
