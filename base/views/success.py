
from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.views.generic import View


class SuccessView(View):
    template_name = 'registration/success.html'
    url = '/account/success/'
    
    def get(self, request):
        return render_to_response(self.template_name)
        


    
