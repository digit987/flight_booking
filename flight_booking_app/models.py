from django.db import models
from django.contrib.auth.models import User

class Flight(models.Model):
    flight_number = models.CharField(max_length=20)
    departure_date = models.DateField()
    departure_time = models.TimeField()

    def __str__(self):
        return f"Flight {self.flight_number} - {self.departure_date} {self.departure_time}"

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=60, default=1)

    def __str__(self):
        return f"Booking for customer {self.user.username} on flight {self.flight.flight_number}"