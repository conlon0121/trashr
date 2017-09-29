from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings


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
    latitude = models.DecimalField(default=0, max_digits=7, decimal_places=3, null=True, blank=True)
    longitude = models.DecimalField(default=0, max_digits=7, decimal_places=3, null=True, blank=True)
    # Whether or not the sensor is sending readings
    functioning = models.BooleanField(default=True)
    utility = models.IntegerField(default=0)

    def __str__(self):
        return str(self.address)
    

class IntervalSet(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)
    dumpster = models.ForeignKey(Dumpster)


    def __str__(self):
        return str(self.timestamp)


class IntervalReading(models.Model):
    angle = models.IntegerField(default=0)
    raw_reading = models.IntegerField(default=0)
    percent_fill = models.DecimalField(default=0, max_digits=5, decimal_places=2)
    interval_set = models.ForeignKey(IntervalSet)

    def __str__(self):
        return str(self.angle)


class UniEvent(models.Model):
    name = models.CharField(max_length=100, default='')
    date = models.DateTimeField(default=timezone.now)
    affected_dumpsters = models.ManyToManyField(Dumpster)


class UserProfile(models.Model):
    name = models.CharField(max_length=100, default='')
    user = models.ForeignKey(User)
    org = models.ForeignKey(Organization)
