from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Organization(models.Model):
    name = models.CharField(max_length=100, default='')
    email = models.EmailField()
    code = models.CharField(max_length=10, default='')

    def __str__(self):
        return self.name


class Dumpster(models.Model):
    # Utility flags
    TRASH = 0
    RECYCLING = 1
    COMPOST = 2
    org = models.ForeignKey(Organization, default=1)
    location = models.CharField(max_length=100, default='')
    address = models.CharField(max_length=100, default='')
    rfid = models.CharField(max_length=50, default='')
    capacity = models.IntegerField(default=0)
    capacity_units = models.CharField(max_length=20, default='')
    container_type = models.CharField(max_length=50, default='')
    coordinates = ArrayField(
        models.DecimalField(max_digits=12, decimal_places=8)
    )
    core_id = models.CharField(max_length=25, default='')
    # Whether or not the sensor is sending readings
    functioning = models.BooleanField(default=True)
    utility = models.PositiveSmallIntegerField(default=0)
    percent_fill = models.SmallIntegerField(default=0)
    alert_percentage = models.SmallIntegerField(default=70)
    last_updated = models.DateTimeField(null=True, blank=True)
    alert_sent = models.BooleanField(default=False)

    def __str__(self):
        return str(self.address)
    
    @property
    def get_utility(self):
        return {
                '0': 'Trash',
                '1': 'Recycling',
                '2': 'Compost'
                }[str(self.utility)]


class IntervalReading(models.Model):
    raw_readings = ArrayField(models.SmallIntegerField(default=0))
    dumpster = models.ForeignKey(Dumpster)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.timestamp) + ' ' + str(self.dumpster)

class Pickup(models.Model):
    dumpster = models.ForeignKey(Dumpster)
    timestamp = models.DateTimeField(auto_now_add=True)


class UserProfile(models.Model):
    user = models.ForeignKey(User)
    org = models.ForeignKey(Organization)

    def __str__(self):
        return self.user.username