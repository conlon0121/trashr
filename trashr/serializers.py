import json
import logging

import time
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from django.utils.timezone import localtime

from trashr.models import Dumpster, Pickup, Alert, Email, Transaction, Subscription
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
        timestamp = localtime(validated_data.get('published_at'))

        agg_reading = 0
        reading_count = 0

        for reading in readings:
            if reading > 0:
                agg_reading = agg_reading + reading
                reading_count += 1

        if agg_reading > 0:
            agg_reading = agg_reading / reading_count
            percent_fill = 100 * (dumpster.capacity - int(agg_reading)) / dumpster.capacity
            if percent_fill < 0:
                logging.getLogger().warning('reading exceeds dumpster capacity')
                percent_fill = 0
            elif percent_fill >= dumpster.alert_percentage and not dumpster.alert_sent:
                dumpster.alert_sent = True
                percent_fill = str(round(percent_fill))
                Alert.objects.create(dumpster=dumpster, fill_percent=percent_fill)
                send_mail(
                    'Dumpster at ' + dumpster.address + ' is ' + percent_fill + '% full.',
                    'Dumpster at ' + dumpster.address
                    + ' is at or above your alert percentage of '
                    + str(dumpster.alert_percentage) + '% as of ' + timestamp.strftime('%D') + " at " +
                    timestamp.strftime("%r") + '.',
                    settings.FROM_EMAIL,
                    list(Email.objects.filter(org=dumpster.org,
                                              receives_alerts=True).values_list('email', flat=True)),
                    fail_silently=False,
                    )

            elif dumpster.percent_fill < percent_fill - 30:
                dumpster.alert_sent = False
                Pickup.objects.create(dumpster=dumpster)
            dumpster.percent_fill = percent_fill
            dumpster.last_updated = timestamp
            dumpster.save()
        logging.getLogger().info('reading created')
        return IntervalReading.objects.create(raw_readings=readings,
                                              dumpster=dumpster,
                                              timestamp=timestamp
                                              )


class TransactionSerializer(serializers.Serializer):

    data = serializers.JSONField()
    type = serializers.ChoiceField(choices=("invoice.created", "invoice.payment_succeeded", "invoice.payment_failed"))

    def create(self, validated_data):
        data = validated_data.get('data')
        invoice_type = validated_data.get('type')
        if invoice_type == 'invoice.created':
            logging.getLogger().info('Transaction created')
            return Transaction.objects.create(subscription=Subscription.objects.get(
                id=data['object']['lines']['data'][0]['subscription']),
                amount=data['object']['amount_due'],
                status='Pending')
        else:
            # Wait five seconds because transaction creation and successful payments come
            # at the same time.
            time.sleep(5)
            transaction = Transaction.objects.filter(subscription=Subscription.objects.get(
                id=data['object']['lines']['data'][0]['subscription']),
                status='Pending').latest('created_datetime')
            if invoice_type == 'invoice.payment_succeeded':
                transaction.status = 'Successful'
                transaction.filled_datetime = timezone.now()
                logging.getLogger().info('Transaction updated')
            elif invoice_type == 'invoice.payment_failed':
                transaction.status = 'Failed'
            transaction.save()
            return transaction
