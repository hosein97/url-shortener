from django.db import models

    
class LinkOwnership(models.Model):

    short_code = models.CharField(
        max_length=10,
        primary_key=True,
    )

    original_url = models.URLField()

    owner_id = models.IntegerField(
        null=True,
        blank=True,
        db_index=True,
    )

    created_at = models.DateTimeField()

    def __str__(self):
        return self.short_code