from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    keycloak_sub = models.CharField(
        max_length=64,
        unique=True,
        db_index=True,
        null=True,
        blank=True,
    )
    email = models.EmailField(
        unique=True,
    )

    def __str__(self):
        return self.username