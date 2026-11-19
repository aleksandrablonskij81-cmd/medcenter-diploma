from django.contrib import admin

from .models import ContactRequest, Doctor, SiteSettings


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Основное", {"fields": ("company_name", "phone", "email", "address", "work_hours", "map_embed_url")}),
        ("Тексты", {"fields": ("about_short", "about_history", "mission")}),
    )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()


@admin.register(ContactRequest)
class ContactRequestAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "email", "created_at", "is_processed")
    list_filter = ("is_processed", "created_at")
    search_fields = ("name", "phone", "email", "message")
    list_editable = ("is_processed",)


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ("full_name", "specialization", "experience_years", "is_active", "order")
    list_filter = ("is_active", "specialization")
    search_fields = ("full_name", "specialization")
    list_editable = ("is_active", "order")
