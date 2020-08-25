from api.payment.models import Payment
from django.contrib import admin
from django.contrib.admin import ModelAdmin

# Register your models here.
class CustomPaymentAdmin(ModelAdmin):

    list_display = (
        "transaction_id",
        "timestamp",
    )
    list_filter = ("timestamp",)

    search_fields = ("customer__name",)
    ordering = ("timestamp",)


admin.site.register(Payment, CustomPaymentAdmin)
