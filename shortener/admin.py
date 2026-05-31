from django.contrib import admin

from .models import ShortURL

# admin.site.register(ShortURL)
@admin.register(ShortURL)
class ShortURLAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "short_code",
        "original_url",
        "clicks",
        "created_at",
    )