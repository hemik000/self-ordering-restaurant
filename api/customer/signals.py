from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
import random

from .models import Customer
from api.table.models import Table
from api.order.models import Order


def generate_session_token(length=10):
    return "".join(
        random.SystemRandom().choice(
            [chr(i) for i in range(97, 123)] + [str(i) for i in range(10)]
        )
        for _ in range(length)
    )


@receiver(post_save, sender=Customer)
def create_customer(sender, instance, created, **kwargs):
    if created:
        table = Table.objects.get(pk=instance.on_table.id)
        print(table)
        table.is_occupied = True
        table.save()
        token = generate_session_token()
        instance.token = token
        instance.save()
