import ast
import logging
import math

from datetime import datetime
from django.utils import timezone
from django.utils.dateparse import parse_datetime

from base.models import Dumpster, IntervalReading
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class CreateReading(APIView):
    #References the model we will be accessing through the API
    queryset = IntervalReading.objects.all()

    def post(self, request, format=None):
        import pdb; pdb.set_trace()
        # Make the string that was sent into a dictionary
        data = ast.literal_eval(request.data['data'])
        timestamp = datetime.strptime(data['published_at'], '%Y-%m-%dT%H:%M:%S.%fZ')\
            .replace(tzinfo=timezone.get_current_timezone())
        data = ast.literal_eval(data['data'])
        dumpster = Dumpster.objects.filter(id=data['dumpster'])
        if dumpster.exists():
            dumpster = dumpster.get()
        else:
            dumpster = Dumpster.objects.create(id=data['dumpster'])
        # Find how full the dumpster is based on the raw reading
        readings = data['readings']
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
            reading = IntervalReading.objects.create(raw_reading=adjusted_reading,
                                                     percent_fill=percent_fill,
                                                     dumpster=dumpster,
                                                     timestamp=timestamp
                                                     )
            logging.getLogger().info('reading created')
        return Response(data, status=status.HTTP_201_CREATED)
