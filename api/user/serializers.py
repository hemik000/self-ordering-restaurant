from rest_framework import serializers, fields
from django.contrib.auth.hashers import make_password
import django.contrib.auth.password_validation as validators
from .models import CustomUser
from django.core import exceptions


class UserCreateSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    def validate(self, data):
        # here data has all the fields which have validated values
        # so we can create a User instance out of it
        print("####### ", data["password2"])

        password2 = data.pop("password2", None)
        if data["password"] != password2:
            raise serializers.ValidationError({"password": "Password must match"})

        user = CustomUser(**data)

        # get the password from the data
        password = data.get("password")

        errors = dict()
        try:
            # validate the password and catch the exception
            validators.validate_password(password=password, user=CustomUser)

        # the exception raised here is different than serializers.ValidationError
        except exceptions.ValidationError as e:
            errors["password"] = list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)

        return super(UserCreateSerializer, self).validate(data)

    def create(self, validated_data):

        print(">>>>>>>>>>>>>>> ", validated_data)
        password = validated_data.pop("password", None)
        # password2 = validated_data.pop("password2", None)
        instance = self.Meta.model(**validated_data)

        if password is not None:
            instance.set_password(password)

        instance.save()
        return instance

    class Meta:
        model = CustomUser
        extra_kwargs = {
            "password": {"write_only": True},
        }
        # exclude = (
        #     "password2",
        #     "is_active",
        #     "is_staff",
        #     "is_superuser",
        # )
        fields = (
            "id",
            "firstName",
            "lastName",
            "email",
            "password",
            "password2",
            "phone_number",
            "gender",
        )


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        extra_kwargs = {
            # "password": {"write_only": True},
        }

        fields = (
            "id",
            "firstName",
            "lastName",
            "email",
            # "password",
            # "password2",
            "phone_number",
            "gender",
            "is_staff",
        )


class UserUpdateSerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):

        # validated_data["is_active"] = True
        # validated_data["is_superuser"] = False
        # validated_data["is_staff"] = False
        print(validated_data)

        password = validated_data.pop("password", None)
        password2 = validated_data.pop("password2", None)

        if password != password2:
            raise serializers.ValidationError({"password": "Password must match"})

        # validated_data.update({"password": password})

        print(validated_data)

        for attr, value in validated_data.items():
            if attr == "password":
                print("#######>>>> ", attr, " ", value)
                instance.set_password(value)
            else:
                setattr(instance, attr, value)

        instance.save()
        return instance

    class Meta:
        model = CustomUser
        extra_kwargs = {
            # "password": {"write_only": True},
        }

        fields = (
            # "id",
            "firstName",
            "lastName",
            "email",
            # "password",
            # "password2",
            "phone_number",
            "gender",
        )


class UserPasswordUpdateSerializer(serializers.ModelSerializer):
    # password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    def update(self, instance, validated_data):
        pass
