from django.contrib import admin
from analytics.models import ClickEvent


@admin.register(ClickEvent)
class ClickEventAdmin(admin.ModelAdmin):
    list_display = (
        "short_code",
        "created_at",
        "ip_address",
        "user_agent",
        "referrer",
    )

    list_filter = ("created_at",)
    search_fields = ("short_code", "ip_address", "user_agent", "referrer")