from django.db import models
from django.conf import settings

class ShortURL(models.Model):

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="short_urls",
    )

    original_url = models.URLField()

    short_code = models.CharField(
        max_length=10,
        unique=True,
    )

    clicks = models.BigIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.short_code