import logging
import ast
import math

from base.models import Dumpster, IntervalReading, IntervalSet
from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class CreateReading(APIView):
    #References the model we will be accessing through the API
    queryset = IntervalReading.objects.all()

    def post(self, request, format=None):
        # Make the string that was sent into a dictionary
        data = ast.literal_eval(request.data['data'])
        dumpster = Dumpster.objects.filter(id=data['dumpster'])
        if dumpster.exists():
            dumpster = dumpster.get()
        else:
            dumpster = Dumpster.objects.create(id=data['dumpster'])
        # Find how full the dumpster is based on the raw reading
        int_set = IntervalSet.objects.create(dumpster=dumpster, timestamp=request.data['published_at'])
        angle = 90 - int(data['readings'][2][0])
        reading = data['readings'][2][1]
        if reading > 0:
            adjusted_reading = reading * math.cos(math.radians(30))
            try:
                percent_fill =  100 * (dumpster.capacity - int(adjusted_reading)) / dumpster.capacity
            except ZeroDivisionError:
                return Response(data, status=400)
            reading = IntervalReading.objects.update_or_create(
                angle=angle,
                raw_reading=adjusted_reading,
                percent_fill=percent_fill,
                interval_set=int_set
            )[0]
        else:
            percent_fill = -1
            adjusted_reading = -1
        for i in range(2):
            try:
                angle = 90 - int(data['readings'][i][0])
                reading = data['readings'][i][1]
                if reading > 0:
                    adjusted_reading = reading * math.cos(math.radians(angle))
                    percent_fill =  100 * (dumpster.capacity - int(adjusted_reading)) / dumpster.capacity
                else:
                    percent_fill = -1
                    adjusted_reading = -1
                reading = IntervalReading.objects.update_or_create(
                    angle=angle,
                    raw_reading=adjusted_reading,
                    percent_fill=percent_fill,
                    interval_set=int_set
                )[0]
            except ZeroDivisionError:
                return Response(data, status=400)
        # logging.getLogger().info('reading created')
        print('reading created')

        return Response(data, status=status.HTTP_201_CREATED)
