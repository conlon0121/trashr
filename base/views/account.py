
from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate

from base.forms import AccountForm


class AccountView(View):
    template_name = 'registration/account.html'
    form_class_select = AccountForm
    url = '/signup/$'
    
    def get(self, request):
        if request.method == 'POST':
            form = AccountForm(request.POST)
            if form.is_valid():
                # Unpack form values
                username = form.cleaned_data['username']
                password = form.cleaned_data['password1']
                #email = form.cleaned_data['email']
                # Create the User record
                user = User(username=username)
                user.set_password(password)
                user.save()
                # Auto login the user
                #user.authenticate(username=username, password=password)
                return HttpResponseRedirect('/accounts/success/')
        else:
            form = AccountForm()

        return render(request, self.template_name, {'form':form})


    def post(self, request):
        if request.method == 'POST':
            form = AccountForm(request.POST)
            if form.is_valid():
                # Unpack form values
                username = form.cleaned_data['username']
                password = form.cleaned_data['password1']
                #email = form.cleaned_data['email']
                # Create the User record
                user = User(username=username)
                user.set_password(password)
                user.save()
                # Auto login the user
                #user.authenticate(username=username, password=password)
                return HttpResponseRedirect('/accounts/success/')
        else:
            form = AccountForm()

        return render(request, self.template_name, {'form':form})
