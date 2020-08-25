from rest_framework import serializers
from rest_framework import fields
from .models import OrderItem
from api.menu.serializers import MenuListSerializers, MenuSerializer


class OrderItemSerializers(serializers.ModelSerializer):
    menu = MenuListSerializers(read_only=True)

    class Meta:
        model = OrderItem
        fields = ("id", "order", "menu", "quantity", "total_amount")


class OrderItemUpdateSerializers(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ("quantity",)

    def update(self, instance, validated_data):
        print(instance)
        print(validated_data)
        instance.quantity = validated_data["quantity"]
        instance.save()
        return instance


class OrderItemCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ("menu", "quantity")

    def create(self, validated_data):
        # print(validated_data)
        order = validated_data["order"]
        menu = validated_data["menu"]
        instance, _ = OrderItem.objects.get_or_create(order=order, menu=menu)
        if _:
            instance.save()
            return instance

        qty = instance.quantity
        more_qty = validated_data["quantity"]
        instance.quantity = int(qty) + int(more_qty)
        instance.save()
        # print(qty, " ", more_qty)
        return instance


class OrderItemSerializer(serializers.ModelSerializer):
    item = serializers.SerializerMethodField()
    final_price = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ("id", "item", "ordered", "quantity", "final_price")

    def get_item(self, obj):
        return MenuSerializer(obj.item).data

    def get_final_price(self, obj):
        return obj.get_final_price()
