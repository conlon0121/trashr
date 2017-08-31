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
    latitude = models.DecimalField(default=0, max_digits=7, decimal_places=3)
    longitude = models.DecimalField(default=0, max_digits=7, decimal_places=3)
    capacity = models.IntegerField(default=10)
    # Whether or not the sensor is sending readings
    functioning = models.BooleanField(default=True)


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
