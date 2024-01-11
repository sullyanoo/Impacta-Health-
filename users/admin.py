from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import DoctorUserProfile, PatientUserProfile, User


class UserAdminConfig(UserAdmin):
    model = User
    search_fields = (
        "email",
        "username",
        "first_name",
    )
    list_filter = ("role", "is_active")
    ordering = ("-date_joined",)
    list_display = ("id", "username", "first_name", "last_name", "email", "is_active", "role")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "username",
                    "first_name",
                )
            },
        ),
        ("Permissions", {"fields": ("is_staff", "is_active")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "role",
                    "email",
                    "username",
                    "first_name",
                    "password1",
                    "password2",
                    "is_active",
                    "is_staff",
                ),
            },
        ),
    )


@admin.register(PatientUserProfile)
class PatientUserProfileInline(admin.ModelAdmin):
    list_display = ["id", "user", "date_of_birth", "cpf", "avatar"]


@admin.register(DoctorUserProfile)
class DoctorUserProfileInline(admin.ModelAdmin):
    list_display = ["id", "user", "date_of_birth", "crm", "avatar"]


admin.site.register(User, UserAdminConfig)
