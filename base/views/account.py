
from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login

from base.forms import AccountForm


class AccountView(View):
    template_name = 'registration/account.html'
    form_class = AccountForm
    url = '/signup/$'
    
    def get(self, request):
        return render(request, self.template_name, {'form_signup':AccountForm()}, {'form_login':AccountForm()})


    def post(self, request):
        form = AccountForm(request.POST)
        if form.is_valid():
            # Unpack form values
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            email = form.cleaned_data['username']
            # Create the User record
            user = User.objects.create_user(username, email, password)
            user.save()
            # Auto login the user
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # A backend authenticated the credentials
                login(request, user)
                return HttpResponseRedirect('/accounts/accountSuccess')
            else:
                return HttpResponseRedirect('/')
        else:
            HttpResponseRedirect(self.url)
