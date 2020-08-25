from django.db import models
import uuid
from django.core.validators import RegexValidator
from api.table.models import Table
from django.core.exceptions import ValidationError

# Create your models here.


class Customer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)

    phone_regex = RegexValidator(
        regex=r"\d{10,10}$", message="Please enter correct phone number.",
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=17)

    on_table = models.ForeignKey(Table, on_delete=models.SET_NULL, null=True)
    is_on_table = models.BooleanField(default=True)
    has_paid = models.BooleanField(default=False)
    token = models.CharField(max_length=10, default=0)
    token = models.CharField(max_length=10, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"

    def clean(self):
        if self.on_table.is_occupied:
            raise ValidationError({"on_table": "Table already in use."})

