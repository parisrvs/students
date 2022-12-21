from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, Student


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {
            "fields": ("first_name", "last_name", "username")
        }),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
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
                    "username",
                    "first_name",
                    "last_name"
                ),
            },
        ),
    )
    list_display = [
        "username", "email", "first_name", "last_name", "is_staff"
    ]
    list_per_page = 10


class StudentAdmin(admin.ModelAdmin):
    list_display = [
        "name", "student_class", "roll_number", "dob", "gender", "mobile"
    ]


admin.site.register(User, UserAdmin)
admin.site.register(Student, StudentAdmin)
