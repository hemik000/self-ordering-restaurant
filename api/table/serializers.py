from rest_framework import serializers
from .models import Table


class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        extra_kwargs = {
            # "password": {"write_only": True},
        }
        fields = ("id", "number", "is_occupied", "is_active")
