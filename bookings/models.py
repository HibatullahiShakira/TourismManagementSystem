from django.db import models
from accomodation.models import Accommodation
from tours.models import Tour
from users.models import User


class Booking(models.Model):
    PAYMENT_STATUS = [
        ('P', 'Pending'),
        ('S', 'Success'),
        ('F', 'Failed'),

    ]
    STATUS = [
        ('B', 'BOOKED'),
        ('S', 'SUSPENDED')
    ]
    booking_date = models.DateField(auto_now_add=True)
    tour_date = models.DateField()
    total_price = models.DecimalField(max_digits=20, decimal_places=2)
    tour = models.ForeignKey(Tour, on_delete=models.PROTECT)
    accommodation = models.ForeignKey(Accommodation, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    payment_status = models.CharField(max_length=1, null=False, blank=False)

    def __str__(self):
        return f""

