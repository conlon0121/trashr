import logging
import ast

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.urls import reverse
from django.utils import timezone
from django.views.generic import TemplateView, View
from django.views.decorators.csrf import csrf_exempt
from base.models import Dumpster, IntervalReading
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
        for i in range(3):
            try:
                percent_fill =  (dumpster.capacity - int(data['readings'][i][1])) / dumpster.capacity
                reading = IntervalReading.objects.update_or_create(
                    angle=data['readings'][i][0],
                    raw_reading=data['readings'][i][1],
                    percent_fill=percent_fill,
                    timestamp=request.data['published_at'],
                    dumpster=dumpster
                )[0]
            except ZeroDivisionError:
                return Response(data, status=400)
        # logging.getLogger().info('reading created')
        print('reading created')
        return Response(data, status=status.HTTP_201_CREATED)

class IndexView(View):
    template_name = "index.html"

    def get(self, request):
        # Get the percent capacity of the latest interval reading for the input dumpster
        percent_capacity = IntervalReading.objects.filter(dumpster__id=1)
        if percent_capacity.exists():
            percent_capacity = int(percent_capacity.latest('timestamp').percent_capacity)
        else:
            percent_capacity = 0
        # TODO: don't subtract 4
        current_hour = timezone.now().hour - 4
        if current_hour >= 17:
            greeting = "Good Evening, Lani"
        elif current_hour > 12:
            greeting = "Good Afternoon, Lani"
        else:
            greeting = "Good Morning, Lani"
        return render_to_response(self.template_name, {'percent_capacity': percent_capacity, 'greeting': greeting})


class HomePageView(View):
    template_name = "logged_in/homepage.html"

    def get(self, request):
        return render_to_response(self.template_name)


class DemoView(View):
    template_name = "old_index.html"

    def get(self, request):
        # Get the percent capacity of the latest interval reading for the input dumpster
        percent_capacity = IntervalReading.objects.filter(dumpster__id=1)
        if percent_capacity.exists():
            percent_capacity = int(percent_capacity.latest('timestamp').percent_capacity)
        else:
            percent_capacity = 0
        # TODO: don't subtract 4
        current_hour = timezone.now().hour - 4
        if current_hour >= 17:
            greeting = "Good Evening, Lani"
        elif current_hour > 12:
            greeting = "Good Afternoon, Lani"
        else:
            greeting = "Good Morning, Lani"
        return render_to_response(self.template_name, {'percent_capacity': percent_capacity, 'greeting': greeting})
