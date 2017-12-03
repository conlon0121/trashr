from django.contrib.gis.db.models import MultiPointField, PointField
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Organization(models.Model):
    name = models.CharField(max_length=100, default='')


class Dumpster(models.Model):
    # Utility flags
    TRASH = 0
    RECYCLING = 1
    COMPOST = 2
    org = models.ForeignKey(Organization, default=1, null=True, blank=True)
    location = models.CharField(max_length=100, default='', null=True, blank=True)
    address = models.CharField(max_length=100, default='', null=True, blank=True)
    rfid = models.CharField(max_length=50, default='', null=True, blank=True)
    capacity = models.IntegerField(default=0, null=True, blank=True)
    capacity_units = models.CharField(max_length=20, default='', null=True, blank=True)
    container_type = models.CharField(max_length=50, default='', null=True, blank=True)
    coordinates = PointField()
    # Whether or not the sensor is sending readings
    functioning = models.BooleanField(default=True)
    utility = models.IntegerField(default=0)
    percent_fill = models.IntegerField(default=0)
    last_updated = models.DateTimeField(null=True, blank=True)

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
    raw_reading = models.IntegerField(default=0)
    dumpster = models.ForeignKey(Dumpster)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.timestamp) + ' ' + str(self.dumpster)


class UniEvent(models.Model):
    name = models.CharField(max_length=100, default='')
    date = models.DateTimeField(default=timezone.now)
    affected_dumpsters = models.ManyToManyField(Dumpster)

    def __str__(self):
        return str(self.date) + ' ' + self.name


class UserProfile(models.Model):
    name = models.CharField(max_length=100, default='')
    user = models.ForeignKey(User)
    org = models.ForeignKey(Organization)

    def __str__(self):
        return self.name


class Route(models.Model):
    driver = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    time_estimate = models.IntegerField()
    number_of_dumpsters = models.IntegerField()
    coordinates = MultiPointField()
    dumpsters = models.ManyToManyField(Dumpster)

    def __str__(self):
        return str(self.date) + ' ' + self.driver