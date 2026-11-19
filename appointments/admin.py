from django.contrib import admin

from .models import Appointment, DiagnosticResult


class DiagnosticResultInline(admin.StackedInline):
    model = DiagnosticResult
    extra = 0
    can_delete = True


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "service", "date", "time", "status", "created_at")
    list_filter = ("status", "date", "service")
    search_fields = ("user__username", "user__email", "service__name")
    list_editable = ("status",)
    inlines = [DiagnosticResultInline]
    date_hierarchy = "date"


@admin.register(DiagnosticResult)
class DiagnosticResultAdmin(admin.ModelAdmin):
    list_display = ("appointment", "created_at")
    search_fields = ("appointment__user__username", "conclusion")