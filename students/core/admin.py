from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from django.db.models import Count, Avg
from django.utils.html import format_html, urlencode
from django.urls import reverse
from .models import User, Student, Result


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


class ResultInline(admin.StackedInline):
    model = Result
    list_select_related = ["student"]
    min_num = 1
    extra = 0


class StudentAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "student_class",
        "roll_number",
        "dob",
        "gender",
        "mobile",
        "results_count",
        "average_marks"
    ]
    search_fields = ["name__istartswith"]
    inlines = [ResultInline]

    @admin.display(ordering="results_count")
    def results_count(self, student):
        url = reverse("admin:core_result_changelist") + '?' + urlencode({
            "student__id": str(student.id)
        })

        return format_html(
            "<a href='{}'>{}</a>",
            url,
            student.results_count
        )

    @admin.display(ordering="average_marks")
    def average_marks(self, student):
        return round(student.average_marks, 2)

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related(
            "results"
        ).annotate(
            results_count=Count("results"),
            average_marks=Avg("results__marks_obtained")
        )


class ResultAdmin(admin.ModelAdmin):
    list_display = [
        "student", "subject", "max_marks", "marks_obtained"
    ]
    list_select_related = ["student"]
    autocomplete_fields = ["student"]


admin.site.register(User, UserAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Result, ResultAdmin)
