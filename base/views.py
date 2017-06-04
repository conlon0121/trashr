from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.urls import reverse
from django.utils import timezone
from django.views.generic import TemplateView, View
from django.views.decorators.csrf import csrf_exempt
from base.models import Dumpster, IntervalReading
from rest_framework import viewsets
from base.serializers import IntervalReadingSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class CreateReading(APIView):
    #References the model we will be accessing through the API
    queryset = IntervalReading.objects.all()

    def post(self, request, format=None):
        # Serialize the data we have received
        serializer = IntervalReadingSerializer(data=request.data)
        #Check if the data is valid
        if serializer.is_valid():
            #Save the serializer to create a reading
            serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

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
        if percent_capacity == 0:
            percent_capacity = "not full"
        else:
            pecent_capacity = "full"
        return render_to_response(self.template_name, {'percent_capacity': percent_capacity, 'greeting': greeting})
