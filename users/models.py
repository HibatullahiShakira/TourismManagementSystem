from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    phone_number = models.CharField(max_length=11, null=False, blank=False)
    age = models.IntegerField(default=18)
    gender = models.CharField(max_length=6, null=False, blank=False)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set'
    )

    def __str__(self):
        return self.username
