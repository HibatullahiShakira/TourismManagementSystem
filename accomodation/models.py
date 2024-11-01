from django.db import models

from tours.models import Tour


class Accommodation(models.Model):
    ACCOMMODATION_CHOICES = [
        ('A', 'ACCOMMODATION'),
        ('S', 'HOME STAYS'),
        ('H', 'HOTELS')
    ]

    location = models.CharField(max_length=50, null=False, blank=False)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    availability = models.BooleanField(default=True)
    images = models.ImageField('images/', null=True, blank=True)
    accommodation_type = models.CharField(max_length=1, choices=ACCOMMODATION_CHOICES, default='HOTELS')
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
