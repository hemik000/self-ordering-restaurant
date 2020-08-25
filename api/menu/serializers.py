from rest_framework import serializers
from .models import Menu


class MenuListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = (
            "id",
            "name",
            "price",
            "category",
            "type",
        )


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = (
            "id",
            "name",
            "description",
            "price",
            "discount_price",
            "image",
            "category",
            "type",
        )
