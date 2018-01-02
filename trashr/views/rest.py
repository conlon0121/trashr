import ast
import logging
import math

from datetime import datetime
from django.core.mail import send_mail
from django.utils import timezone

from trashr.models import Dumpster, IntervalReading, Pickup
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class CreateReading(APIView):
    #References the model we will be accessing through the API
    queryset = IntervalReading.objects.all()

    def post(self, request, format=None):
        # Make the string that was sent into a dictionary
        data = ast.literal_eval(request.data['data'])
        timestamp = datetime.strptime(request.data['published_at'], '%Y-%m-%dT%H:%M:%S.%fZ') \
            .replace(tzinfo=timezone.get_current_timezone())
        try:
            dumpster = Dumpster.objects.get(id=data['dumpster'])
        except Dumpster.DoesNotExist:
            dumpster = Dumpster.objects.create(id=data['dumpster'])
        # Find how full the dumpster is based on the raw reading
        readings = data['readings']
        for reading in readings:
            if reading > 0:
                adjusted_reading = reading * math.cos(math.radians(30))
                try:
                    percent_fill =  100 * (dumpster.capacity - int(adjusted_reading)) / dumpster.capacity
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
                    return Response(data, status=400)
            else:
                percent_fill = -1
                adjusted_reading = -1
            dumpster.percent_fill = percent_fill
            dumpster.last_updated = timestamp
            dumpster.save()
            IntervalReading.objects.create(raw_reading=adjusted_reading,
                                           dumpster=dumpster,
                                           timestamp=timestamp
                                           )
            logging.getLogger().info('reading created')
        return Response(data, status=status.HTTP_201_CREATED)
