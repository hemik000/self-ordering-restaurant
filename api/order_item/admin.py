from django.contrib import admin
from .models import OrderItem
from django.contrib.admin import ModelAdmin

# Register your models here.


class CustomOrderItemAdmin(ModelAdmin):

    list_display = ("item", "customer", "on_table", "status")
    list_filter = ("status", "customer__on_table")

    search_fields = ("customer__name",)

    ordering = ("status",)

    def on_table(self, instance):
        return instance.customer.on_table.number


admin.site.register(OrderItem, CustomOrderItemAdmin)
