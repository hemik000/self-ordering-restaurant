from api.coupon.serializers import CouponSerializer
from api.order_item.serializers import OrderItemSerializer
from rest_framework import serializers
from .models import Order


# class OrderSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Order
#         extra_kwargs = {
#             # "password": {"write_only": True},
#         }
#         depth = 1

#         fields = ("id", "table", "customer", "sub_total", "ugst", "cgst", "grand_total")

#     def create(self, validated_data):
#         instance = self.Meta.model(**validated_data)
#         instance.save()
#         return instance


# class OrderCreateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Order
#         extra_kwargs = {
#             # "password": {"write_only": True},
#         }
#         # depth = 1

#         fields = (
#             "id",
#             "menu",
#         )


class OrderSerializer(serializers.ModelSerializer):
    order_items = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()
    discount = serializers.SerializerMethodField()
    cgst = serializers.SerializerMethodField()
    sgst = serializers.SerializerMethodField()
    grand_total = serializers.SerializerMethodField()
    coupon = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%d-%m-%Y %I:%M:%p")

    class Meta:
        model = Order
        fields = (
            "id",
            "order_items",
            "invoice_no",
            "coupon",
            "total",
            "discount",
            "cgst",
            "sgst",
            "grand_total",
            "payment_type",
            "created_at",
        )

    def get_order_items(self, obj):
        print(obj)
        return OrderItemSerializer(obj.items.all(), many=True).data

    def get_total(self, obj):
        return obj.get_total()

    def get_discount(self, obj):
        return obj.coupon_discount()

    def get_cgst(self, obj):
        return obj.get_cgst()

    def get_sgst(self, obj):
        return obj.get_sgst()

    def get_grand_total(self, obj):
        return obj.get_total_after_gst()

    def get_coupon(self, obj):
        if obj.coupon is not None:
            return CouponSerializer(obj.coupon).data
        return None
