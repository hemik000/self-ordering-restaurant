from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
import uuid
from django.core.validators import RegexValidator
from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    email = models.EmailField(_("Email address"), unique=True)
    firstName = models.CharField(_("First Name"), max_length=50)
    lastName = models.CharField(_("Last Name"), max_length=50)

    phone_regex = RegexValidator(
        regex=r"\d{10,10}$", message="Please enter correct phone number.",
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)

    GENDER_CHOICE = (("M", "Male"), ("F", "Female"))
    gender = models.CharField(max_length=1, choices=GENDER_CHOICE)

    is_staff = models.BooleanField(default=False)
    # is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
