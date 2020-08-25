from rest_framework.response import Response
from api.payment.models import Payment
from api.customer.models import Customer
from api.table.models import Table
from .serializers import GetTotalRevenueSerializer
from rest_framework.views import APIView
from datetime import datetime
from django.db.models import Sum
from rest_framework.status import HTTP_200_OK
from rest_framework.permissions import IsAuthenticated


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
