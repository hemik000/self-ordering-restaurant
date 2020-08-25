from rest_framework import serializers
from .models import Customer
from api.table.models import Table


class CreatCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        extra_kwargs = {
            # "password": {"write_only": True},
        }

        fields = ("id", "name", "phone_number", "on_table", "token")

    def create(self, validated_data):
        print(validated_data["on_table"].id)
        table = Table.objects.get(id=validated_data["on_table"].id)

        if table.is_occupied:
            raise serializers.ValidationError({"on_table": "Table already in use."})

        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance


class DetailCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        extra_kwargs = {
            # "password": {"write_only": True},
        }

        fields = ("id", "name", "phone_number", "on_table", "token")
