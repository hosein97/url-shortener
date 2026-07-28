from django.contrib import admin

from analytics.models import LinkOwnership


@admin.register(LinkOwnership)
class LinkOwnershipAdmin(admin.ModelAdmin):

    list_display = (
        "short_code",
        "owner_id",
        "created_at",
    )

    list_filter = (
        "created_at",
    )

    search_fields = (
        "short_code",
        "owner_id",
    )

    ordering = (
        "-created_at",
    )