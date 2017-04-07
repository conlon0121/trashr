from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.urls import reverse
from django.utils import timezone
from django.views.generic import TemplateView, View
from django.views.decorators.csrf import csrf_exempt
from trashr_dev.models import Dumpster


class IndexView(View):
    template_name = "index.html"

    @csrf_exempt
    def get(self, request):
        percent = Dumpster.objects.first().percent_capacity
        current_hour = timezone.now().hour - 4
        if current_hour >=17:
            greeting = "Good Evening, Lani"
        elif current_hour > 12:
            greeting = "Good Afternoon, Lani"
        else:
            greeting = "Good Morning, Lani"
        if percent == 0:
            percent_capacity = "not full"
        else:
            pecent_capacity = "full"
        return render_to_response(self.template_name, {'percent_capacity': percent_capacity, 'greeting': greeting})
    
    @csrf_exempt
    def post(self, request):
        data = request.POST.get('data')
        dumpster = Dumpster.objects.first() 
        dumpster.percent_capacity = data
        dumpster.save()
        return HttpResponse(200)
