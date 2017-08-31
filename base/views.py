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
import ast


class CreateReading(APIView):
    #References the model we will be accessing through the API
    queryset = IntervalReading.objects.all()

    def post(self, request, format=None):
        # Make the string that was sent into a dictionary
        data = ast.literal_eval(request.data['data'])
        print(data)
        dumpster = Dumpster.objects.filter(id=data['dumpster'])
        if dumpster.exists():
            dumpster = dumpster.get()
        else:
            dumpster = Dumpster.objects.create(
                    id=data['dumpster'],
                    latitude=data['latitude'],
                    longitude=data['longitude'],
                    capacity=data['raw_reading']
                    )
        # Find how full the dumpster is based on the raw reading
        percent_capacity =  (dumpster.capacity - int(data['raw_reading'])) / dumpster.capacity
        reading = IntervalReading.objects.update_or_create(
            raw_reading=data['raw_reading'],
            percent_capacity=percent_capacity,
            timestamp=request.data['published_at'],
            dumpster=dumpster
        )[0]
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
