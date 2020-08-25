from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = (
        "email",
        "is_staff",
        "is_active",
    )
    list_filter = (
        "is_staff",
        "is_active",
    )

    readonly_fields = ["last_login", "date_joined", "updated_at"]

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Personal Data",
            {"fields": ("firstName", "lastName", "phone_number", "gender")},
        ),
        ("Permissions", {"fields": ("is_staff", "is_active", "is_superuser")}),
        ("Information", {"fields": ("last_login", "date_joined", "updated_at")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "firstName",
                    "lastName",
                    "phone_number",
                    "gender",
                    "is_staff",
                    "is_active",
                    "is_superuser",
                ),
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)


admin.site.register(CustomUser, CustomUserAdmin)
