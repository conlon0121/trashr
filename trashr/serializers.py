import json
import logging
import math

from django.conf import settings
from django.core.mail import send_mail

from trashr.models import Dumpster, Pickup, Alert, UserProfile, Email
from trashr.models import IntervalReading
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class ReadingSerializer(serializers.Serializer):
    data = serializers.JSONField()
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
        reading_count = 0
        for reading in readings:
            if reading > 0:
                agg_reading = agg_reading + reading
                reading_count += 1
        IntervalReading.objects.create(raw_readings=readings,
                                       dumpster=dumpster,
                                       timestamp=timestamp
                                       )
        if agg_reading < 0:
            agg_reading = agg_reading / reading_count
            percent_fill = 100 * (dumpster.capacity - int(agg_reading)) / dumpster.capacity
            if percent_fill >= dumpster.alert_percentage and not dumpster.alert_sent:
                dumpster.alert_sent = True
                rounded_fill = str(round(percent_fill))
                Alert.objects.create(dumpster=dumpster, fill_percent=rounded_fill)
                send_mail(
                    'Dumpster at ' + dumpster.address + ' is ' + rounded_fill + '% full.',
                    'Dumpster at ' + dumpster.address
                    + 'is at or above your alert percentage of '
                    + str(dumpster.alert_percentage) + '% as of ' + timestamp.strftime('%D') + '.',
                    settings.FROM_EMAIL,
                    [list(Email.objects.filter(org=dumpster.org,
                                               receives_alerts=True).values_list('email', flat=True))],
                    fail_silently=False,
                    )
            elif dumpster.percent_fill < percent_fill - 30:
                dumpster.alert_sent = False
                Pickup.objects.create(dumpster=dumpster)
            dumpster.save()
        logging.getLogger().info('reading created')
        return IntervalReading.objects.create(raw_readings=readings,
                                              dumpster=dumpster,
                                              timestamp=timestamp
                                              )
