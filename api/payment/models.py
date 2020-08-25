import uuid
from api.customer.models import Customer
from django.db import models

# Create your models here.
class Payment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    transaction_id = models.CharField(max_length=255, default=0)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.transaction_id
