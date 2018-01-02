from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login

from trashr.forms import CompanyCodeForm


class CompanycodeView(View):
    template_name = 'logged_in/companyCode.html'
    form_class_select = CompanyCodeForm
    url = '/companyCode/$'
    
    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        if request.method == 'POST':
            form = CompanyCodeForm(request.POST)
            if(form.is_valid()):
                companyCode = form.cleaned_data['companyCode']
                return HttpResponseRedirect('/preferences/')
            
        else:
            form = CompanyCodeForm()

        return render(request, self.template_name, {'form_companyCode':form})
