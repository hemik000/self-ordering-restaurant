from api.customer.models import Customer
from django.db import models
import uuid
from api.menu.models import Menu

# Create your models here.
STATUS = (
    ("pending", "Pending"),
    ("in_process", "In Process"),
    ("serve", "Serve"),
    ("cancel", "Cancel"),
)


class OrderItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Menu, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    status = models.CharField(choices=STATUS, max_length=15, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.item)

    def get_total_item_price(self):
        return round(self.quantity * self.item.price, 2)

    def get_total_discount_item_price(self):
        return round(self.quantity * self.item.discount_price, 2)

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()
