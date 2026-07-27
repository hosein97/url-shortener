from django.db import models


class ClickEvent(models.Model):

    short_code = models.CharField(
        max_length=10,
        db_index=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    ip_address = models.GenericIPAddressField(
        null=True
    )

    user_agent = models.TextField(
        null=True
    )

    referrer = models.TextField(
        null=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.short_code}"
    
    
    


class LinkOwnership(models.Model):

    short_code = models.CharField(
        max_length=10,
        unique=True,
        db_index=True,
    )

    owner_id = models.IntegerField(
        db_index=True,
    )

    created_at = models.DateTimeField()

    def __str__(self):
        return self.short_code