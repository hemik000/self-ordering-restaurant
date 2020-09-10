from api.order_item.models import OrderItem
from api.order_item.serializers import OrderItemSerializer
from api.customer.models import Customer
from rest_framework import serializers
from rest_framework import fields
from api.payment.models import Payment
from api.order.models import Order
from api.coupon.serializers import CouponSerializer


class GetActiveCustomerSerializer(serializers.ModelSerializer):

    orders = serializers.SerializerMethodField()
    customer = serializers.SerializerMethodField()
    table = serializers.SerializerMethodField()
    customer_token = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ("id", "customer", "table", "orders", "customer_token")

    def get_orders(self, obj):
        return obj.items_counts()

    def get_customer(self, obj):
        return obj.customer.name

    def get_table(self, obj):
        return obj.table.number

    def get_customer_token(self, obj):
        return obj.customer.token


class OrderDetailSerializer(serializers.ModelSerializer):
    customer = serializers.SerializerMethodField()
    customer_token = serializers.SerializerMethodField()
    item_count = serializers.SerializerMethodField()
    table = serializers.SerializerMethodField()
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
            "customer",
            "table",
            "item_count",
            "order_items",
            "invoice_no",
            "otp",
            "customer_token",
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

    def get_item_count(self, obj):
        return obj.items_counts()

    def get_customer(self, obj):
        return obj.customer.name

    def get_customer_token(self, obj):
        return obj.customer.token


    def get_table(self, obj):
        return obj.table.number

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


class OrderItemSymmarySerializers(serializers.ModelSerializer):

    item = serializers.SerializerMethodField()
    table = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ("item", "table", "quantity", "status")

    def get_item(self, obj):
        return obj.item.name

    def get_table(self, obj):
        return obj.customer.on_table.number


class OrderHistorySerializers(serializers.ModelSerializer):
    customer = serializers.SerializerMethodField()
    item_count = serializers.SerializerMethodField()
    cgst = serializers.SerializerMethodField()
    sgst = serializers.SerializerMethodField()
    grand_total = serializers.SerializerMethodField()
    payment = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%d-%m-%Y %I:%M:%p")

    class Meta:
        model = Order
        fields = (
            "id",
            "invoice_no",
            "customer",
            "item_count",
            "cgst",
            "sgst",
            "grand_total",
            "payment_type",
            "payment",
            "created_at",
        )

    def get_item_count(self, obj):
        return obj.items_counts()

    def get_customer(self, obj):
        return obj.customer.name

    def get_cgst(self, obj):
        return obj.get_cgst()

    def get_sgst(self, obj):
        return obj.get_sgst()

    def get_grand_total(self, obj):
        return obj.get_total_after_gst()

    def get_payment(self, obj):
        return obj.payment.transaction_id


class OrderHistoryExportSerializers(serializers.ModelSerializer):
    customer = serializers.SerializerMethodField()
    item_count = serializers.SerializerMethodField()
    cgst = serializers.SerializerMethodField()
    sgst = serializers.SerializerMethodField()
    grand_total = serializers.SerializerMethodField()
    payment = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = (
            "invoice_no",
            "customer",
            "item_count",
            "cgst",
            "sgst",
            "grand_total",
            "payment",
        )

    def get_item_count(self, obj):
        return obj.items_counts()

    def get_customer(self, obj):
        return obj.customer.name

    def get_cgst(self, obj):
        return obj.get_cgst()

    def get_sgst(self, obj):
        return obj.get_sgst()

    def get_grand_total(self, obj):
        return obj.get_total_after_gst()

    def get_payment(self, obj):
        return obj.payment.transaction_id
