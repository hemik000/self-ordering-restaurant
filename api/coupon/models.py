from django.db import models
import uuid

# Create your models here.
class Coupon(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=15)
    percent = models.FloatField()
    is_active = models.BooleanField(default=True)
    multiple_use = models.BooleanField(default=False)

    def __str__(self):
        return self.code
