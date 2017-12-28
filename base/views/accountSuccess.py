from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.views.generic import View


class AccountSuccessView(View):
    template_name = 'registration/accountSuccess.html'
    url = '/accounts/accountSuccess/'
    
    def get(self, request):
        return render_to_response(self.template_name)
        


    
