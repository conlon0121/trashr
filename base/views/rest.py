import ast
import logging
import math

from datetime import datetime
from django.utils import timezone

from base.models import Dumpster, IntervalReading
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class CreateReading(APIView):
    #References the model we will be accessing through the API
    queryset = IntervalReading.objects.all()

    def post(self, request, format=None):
        # Make the string that was sent into a dictionary
        data = ast.literal_eval(request.data['data'])
        timestamp = datetime.strptime(request.data['published_at'], '%Y-%m-%dT%H:%M:%S.%fZ')\
            .replace(tzinfo=timezone.get_current_timezone())
        try:
            dumpster = Dumpster.objects.get(id=data['dumpster'])
        except Dumpster.DoesNotExist:
            dumpster = Dumpster.objects.create(id=data['dumpster'])
        # Find how full the dumpster is based on the raw reading
        readings = data['readings']
        import pdb; pdb.set_trace()
        for reading in readings:
            if reading > 0:
                adjusted_reading = reading * math.cos(math.radians(30))
                try:
                    percent_fill =  100 * (dumpster.capacity - int(adjusted_reading)) / dumpster.capacity
                except ZeroDivisionError:
                    return Response(data, status=400)
            else:
                percent_fill = -1
                adjusted_reading = -1
            dumpster.percent_fill = percent_fill
            dumpster.last_updated = timestamp
            dumpster.save()
            reading = IntervalReading.objects.create(raw_reading=adjusted_reading,
                                                     dumpster=dumpster,
                                                     timestamp=timestamp
                                                     )
            logging.getLogger().info('reading created')
        return Response(data, status=status.HTTP_201_CREATED)
