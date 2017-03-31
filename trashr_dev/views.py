from django.views.generic import TemplateView, View
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.shortcuts import render_to_response
from django.http import HttpResponse


class IndexView(View):
    template_name = "index.html"
    data = 5

    @csrf_exempt
    def get(self, request):
        data = self.data
        return render_to_response(self.template_name, {'data': data})
    
    @csrf_exempt
    def post(self, request):
        self.data = request.POST.get('data')
        return HttpResponse(200)
