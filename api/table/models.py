from django.db import models
import uuid


# Create your models here.


class Table(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    number = models.IntegerField(("Table Number"), unique=True)
    is_active = models.BooleanField(default=True)
    is_occupied = models.BooleanField(default=False)

    def __str__(self):
        return "Table Number: " + str(self.number)

    class Meta:
        verbose_name = "Table"
        verbose_name_plural = "Tables"
