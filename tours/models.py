from django.db import models


class Tour(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    description = models.CharField(max_length=1500, null=False, blank=False)
    location = models.CharField(max_length=100, null=False, blank=False)
    images = models.ImageField('images/', null=True, blank=True)
    price = models.DecimalField(max_digits=20, decimal_places=2, null=False, blank=False)
    availability = models.BooleanField(default=True)
