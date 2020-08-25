from rest_framework import serializers
from rest_framework import fields
from api.payment.models import Payment


class GetTotalRevenueSerializer(serializers.ModelSerializer):
    model = Payment
    fields = ("amount",)
