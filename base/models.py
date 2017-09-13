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
    org = models.ForeignKey(Organization, default=1)
    location = models.CharField(max_length=100, default='')
    address = models.CharField(max_length=100, default='')
    rfid = models.CharField(max_length=50, default='')
    capacity = models.IntegerField(default=0)
    capacity_units = models.CharField(max_length=20, default='')
    container_type = models.CharField(max_length=50, default='')
    latitude = models.DecimalField(default=0, max_digits=7, decimal_places=3)
    longitude = models.DecimalField(default=0, max_digits=7, decimal_places=3)
    # Whether or not the sensor is sending readings
    functioning = models.BooleanField(default=True)

    def __str__(self):
        return str(self.address)


class IntervalReading(models.Model):
    raw_reading = models.IntegerField(default=0)
    percent_capacity = models.DecimalField(default=0, max_digits=5, decimal_places=2)
    timestamp = models.DateTimeField(default=timezone.now)
    dumpster = models.ForeignKey(Dumpster)

    def __str__(self):
        return str(self.timestamp)


class UniEvent(models.Model):
    name = models.CharField(max_length=100, default='')
    date = models.DateTimeField(default=timezone.now)
    affected_dumpsters = models.ManyToManyField(Dumpster)


class UserProfile(models.Model):
    name = models.CharField(max_length=100, default='')
    user = models.ForeignKey(User)
    org = models.ForeignKey(Organization)
