import logging
import ast
import math

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.urls import reverse
from django.utils import timezone
from django.views.generic import TemplateView, View
from django.views.decorators.csrf import csrf_exempt
from base.models import Dumpster, IntervalReading, IntervalSet
from base.serializers import IntervalReadingSerializer
from rest_framework import status, viewsets
from rest_framework.exceptions import ValidationError
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
        for i in range(3):
            try:
                reading = data['readings'][i][1]
                angle = int(data['readings'][i][0])
                if angle == 34:
                    angle = 36
                elif angle == 52:
                    angle = 54
                angle = 90 - angle
                if reading > 0:
                    adjusted_reading = data['readings'][i][1] * math.cos(math.radians(angle))
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

class IndexView(View):
    template_name = "index.html"

    def get(self, request):
        return render_to_response(self.template_name)


class HomePageView(View):
    template_name = "logged_in/homepage.html"

    def get(self, request):
        return render_to_response(self.template_name)


class DemoView(View):
    template_name = "old_index.html"

    def get(self, request):
        # Get the percent capacity of the latest interval reading for the input dumpster
        current_hour = timezone.localtime(timezone.now()).hour
        if current_hour >= 17:
            greeting = "Good Evening, Lani"
        elif current_hour > 12:
            greeting = "Good Afternoon, Lani"
        else:
            greeting = "Good Morning, Lani"
        try:
            int_set = IntervalSet.objects.filter(dumpster__id=1).latest('timestamp')
            timestamp = timezone.localtime(int_set.timestamp)
            percent_fill = 0
            count = 0
            for reading in int_set.intervalreading_set.all():
                if reading.angle != 36 and reading.raw_reading != -1:
                    percent_fill += int(reading.percent_fill)
                    count += 1
            percent_fill = percent_fill / count
        except (IntervalSet.DoesNotExist, ZeroDivisionError):
            percent_fill = 0
            timestamp = None
        return render_to_response(self.template_name, {'percent_fill': round(percent_fill, 1), 'greeting': greeting, 'timestamp': timestamp})
