from api.coupon.models import Coupon
from api.order_item.models import OrderItem
from django.db import models
import uuid
from api.table.models import Table
from api.customer.models import Customer
from api.menu.models import Menu
from django.db.models import Sum
from api.payment.models import Payment
import random, math

# Create your models here.
def increment_invoice_number():
    last_invoice = Order.objects.all().order_by("created_at").last()
    if not last_invoice:
        return "HT1000"
    invoice_no = last_invoice.invoice_no
    invoice_int = invoice_no.split("HT")[-1]

    new_invoice_int = int(invoice_int) + 1
    new_invoice_no = "HT" + str(new_invoice_int)
    return new_invoice_no


def generateOTP():

    # Declare a digits variable
    # which stores all digits
    digits = "0123456789"
    OTP = ""

    # length of password can be chaged
    # by changing value in range
    for i in range(6):
        OTP += digits[math.floor(random.random() * 10)]

    return OTP


PAYMENT_TYPE = (("online", "Online"), ("cash", "Cash"))


class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    table = models.ForeignKey(Table, on_delete=models.SET_NULL, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    items = models.ManyToManyField(OrderItem)
    ordered = models.BooleanField(default=False)
    payment = models.ForeignKey(
        Payment, on_delete=models.SET_NULL, max_length=5, null=True, blank=True
    )
    payment_type = models.CharField(
        choices=PAYMENT_TYPE, max_length=10, default="online"
    )
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, blank=True, null=True)
    invoice_no = models.CharField(
        max_length=500, default=increment_invoice_number, unique=True
    )
    otp = models.IntegerField(default=generateOTP)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.invoice_no

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        # if self.coupon:
        #     total -= round(total * self.coupon.percent / 100, 2)
        #     print(total)
        return total

    def coupon_discount(self):
        discount = 0
        if self.coupon:
            discount = round(self.get_total() * self.coupon.percent / 100, 2)
            return discount
        return discount

    def get_cgst(self):
        total = self.get_total() - self.coupon_discount()
        return round(total * 2.5 / 100, 2)

    def get_sgst(self):
        total = self.get_total() - self.coupon_discount()
        return round(total * 2.5 / 100, 2)

    def get_total_after_gst(self):
        total = self.get_total() - self.coupon_discount()
        cgst = self.get_cgst()
        sgst = self.get_sgst()
        return round(total + (cgst + sgst), 2)

    def items_counts(self):
        return self.items.count()

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"

