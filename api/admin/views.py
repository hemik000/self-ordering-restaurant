from api.order_item.models import OrderItem
from api.order.models import Order
from .serializers import (
    GetActiveCustomerSerializer,
    OrderDetailSerializer,
    OrderHistoryExportSerializers,
    OrderHistorySerializers,
    OrderItemSymmarySerializers,
)
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from api.payment.models import Payment
from api.customer.models import Customer
from api.table.models import Table
from django.http import Http404

# from .serializers import GetTotalRevenueSerializer
from rest_framework.views import APIView
from datetime import datetime
from django.db.models import Sum
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet
from drf_renderer_xlsx.mixins import XLSXFileMixin
from drf_renderer_xlsx.renderers import XLSXRenderer
from rest_pandas import PandasView, PandasExcelRenderer


class GetDashboardStats(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        today = datetime.now()

        today_customer = Customer.objects.filter(
            created_at__date=datetime.date(today), has_paid=True
        )

        table_busy = Table.objects.filter(is_occupied=True)

        pay_today = Payment.objects.filter(timestamp__date=datetime.date(today))
        total_today = pay_today.aggregate(Sum("amount"))

        pay_month = Payment.objects.filter(timestamp__month=today.month)
        total_month = pay_month.aggregate(Sum("amount"))
        return Response(
            {
                "customer_today": today_customer.count(),
                "table_busy": table_busy.count(),
                "today": total_today["amount__sum"],
                "thismonth": total_month["amount__sum"],
            },
            status=HTTP_200_OK,
        )


class GetActiveCustomerView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GetActiveCustomerSerializer

    def get_queryset(self):
        try:
            order = Order.objects.filter(ordered=False)
            return order
        except Order.DoesNotExist:
            raise Http404("No Orders Yet")


class GetOrderDetailView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderDetailSerializer
    queryset = Order.objects.all()


class ChangeOrderItemView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        item_id = request.data.get("item_id", None)

        if item_id is None:
            return Response(
                {"detail": "Invalid data received"}, status=HTTP_400_BAD_REQUEST
            )

        order_item = OrderItem.objects.filter(pk=item_id)
        print(order_item[0].ordered)
        order_item.update(ordered=not order_item[0].ordered)
        # order_item.save()
        return Response(status=HTTP_200_OK)


class OrderItemSummary(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderItemSymmarySerializers
    # queryset = OrderItem.objects.all()

    def get_queryset(self):
        try:
            order = OrderItem.objects.filter(ordered=True, status="pending")
            return order
        except OrderItem.DoesNotExist:
            raise Http404("No Orders Yet")


class TestHome(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class_OrderItem = OrderItemSymmarySerializers
    serializer_class_ActiveOrder = GetActiveCustomerSerializer
    queryset = ""

    def get_queryset_OrderItem(self):
        try:
            order = OrderItem.objects.filter(ordered=True, status="pending").order_by(
                "created_at"
            )
            return order
        except OrderItem.DoesNotExist:
            raise Http404("No Orders Yet")

    def get_queryset_ActiveOrder(self):
        try:
            order = Order.objects.filter(ordered=False).order_by("created_at")
            return order
        except Order.DoesNotExist:
            raise Http404("No Active Orders Yet")

    def list(self, request, *args, **kwargs):

        today = datetime.now()

        today_customer = Customer.objects.filter(
            created_at__date=datetime.date(today), has_paid=True
        )

        table_busy = Table.objects.filter(is_occupied=True)

        pay_today = Payment.objects.filter(timestamp__date=datetime.date(today))
        total_today = pay_today.aggregate(Sum("amount"))

        pay_month = Payment.objects.filter(timestamp__month=today.month)
        total_month = pay_month.aggregate(Sum("amount"))
        # return Response(
        stats = (
            {
                "customer_today": today_customer.count(),
                "table_busy": table_busy.count(),
                "today": total_today["amount__sum"],
                "thismonth": total_month["amount__sum"],
            },
        )
        #     status=HTTP_200_OK,
        # )

        order_item = self.serializer_class_OrderItem(
            self.get_queryset_OrderItem(), many=True
        )
        orders = self.serializer_class_ActiveOrder(
            self.get_queryset_ActiveOrder(), many=True
        )
        return Response(
            {"stats": stats, "orders": orders.data, "order_items": order_item.data},
            status=HTTP_200_OK,
        )


class GetOrderHistoryView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderHistorySerializers

    def get_queryset(self):
        try:

            date_time_str = self.request.query_params.get("date", None)
            # date_time_str = self.request.get("date", None)
            if date_time_str is None:
                raise Http404("No Orders Yet")
            date_time_obj = datetime.strptime(date_time_str, "%d-%m-%Y")
            order = Order.objects.filter(
                ordered=True, created_at__date=date_time_obj.date()
            )
            return order
        except Order.DoesNotExist:
            raise Http404("No Orders Yet")


class MyOrderExportViewSet(PandasView):
    serializer_class = OrderHistoryExportSerializers
    permission_classes = [IsAuthenticated]
    renderer_classes = [PandasExcelRenderer]
    file_name = "order.xlsx"

    def get_pandas_filename(self, request, format):
        if format in ("xls", "xlsx"):
            # Use custom filename and Content-Disposition header
            return "Order Export"  # Extension will be appended automatically
        else:
            # Default filename from URL (no Content-Disposition header)
            return None

    def get_queryset(self):
        try:
            date_time_str = self.request.query_params.get("date", None)
            # date_time_str = self.request.get("date", None)
            if date_time_str is None:
                raise Http404("No Orders Yet")
            date_time_obj = datetime.strptime(date_time_str, "%d-%m-%Y")
            order = Order.objects.filter(
                ordered=True, created_at__date=date_time_obj.date()
            )
            return order
        except Order.DoesNotExist:
            raise Http404("No Orders Yet")