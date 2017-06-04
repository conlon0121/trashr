from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings

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
        return str(self.timestamp)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
