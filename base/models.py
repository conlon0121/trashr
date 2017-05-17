from django.db import models
from django.utils import timezone

class Dumpster(models.Model):
    latitude = models.DecimalField(default=0, max_digits=7, decimal_places=3)
    longitude = models.DecimalField(default=0, max_digits=7, decimal_places=3)
    capacity = models.IntegerField(default=10)

class IntervalReading(models.Model):
    raw_reading = models.IntegerField(default=0)
    percent_capacity = models.DecimalField(default=0, max_digits=5, decimal_places=2)
    timestamp = models.DateTimeField(default=timezone.now)
    dumpster = models.ForeignKey(Dumpster)

    def __str__(self):
        return self.percent_capacity
