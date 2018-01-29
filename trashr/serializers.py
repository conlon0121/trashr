import json
import logging
import math

from django.core.mail import send_mail

from trashr.models import Dumpster, Pickup
from trashr.models import IntervalReading
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class ParticleSerializer(serializers.Serializer):
    name = serializers.CharField()
    data = serializers.JSONField()
    ttl = serializers.CharField()
    published_at = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%S.%fZ')
    coreid = serializers.CharField(max_length=25)

    def create(self, validated_data):
        try:
            dumpster = Dumpster.objects.get(core_id=validated_data.get('coreid'))
        except Dumpster.DoesNotExist:
            raise ValidationError("Dumpster Does not exist")
        readings = json.loads(validated_data.get('data'))['readings']
        timestamp = validated_data.get('published_at')
        agg_reading = 0
        for reading in readings:
            if reading > 0:
                agg_reading = agg_reading + reading * math.cos(math.radians(10))
        try:
            percent_fill =  100 * (dumpster.capacity - int(agg_reading)) / dumpster.capacity
            if percent_fill >= dumpster.alert_percentage and not dumpster.alert_sent:
                dumpster.alert_sent = True
                rounded_fill = str(round(percent_fill))
                send_mail(
                    'Dumpster at ' + dumpster.address + 'is ' + rounded_fill + 'full.',
                    'Dumpster at ' + dumpster.address
                    + 'is at or above your alert percentage of '
                    + str(dumpster.alert_percentage) + ' as of ' + str(timestamp) + '.',
                    'trashrwaste@gmail.com',
                    [dumpster.org.email],
                    fail_silently=False,
                    )
            elif dumpster.percent_fill < percent_fill - 30:
                dumpster.alert_sent = False
                Pickup.objects.create(dumpster=dumpster)
        except ZeroDivisionError:
            pass
        dumpster.save()
        logging.getLogger().info('reading created')
        return IntervalReading.objects.create(raw_readings=readings,
                                              dumpster=dumpster,
                                              timestamp=timestamp
                                              )
