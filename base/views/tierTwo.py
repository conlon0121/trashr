from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.views.generic import View


class TierTwoView(View):
    template_name = 'tierTwo.html'
    
    def get(self, request):
        return render_to_response(self.template_name)
        


    
