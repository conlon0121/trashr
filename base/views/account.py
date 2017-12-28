
from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login

from base.forms import AccountForm


class AccountView(View):
    template_name = 'registration/account.html'
    form_class_select = AccountForm
    url = '/signup/$'
    
    def get(self, request):
        return render(request, self.template_name, {'form_signup':AccountForm()}, {'form_login':form})


    def post(self, request):
<<<<<<< HEAD
        if request.method == 'POST':
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
=======
        form = AccountForm(request.POST)
        if form.is_valid():
            # Unpack form values
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            email = form.cleaned_data['username']
            firstName = form.cleaned_data['first_name']
            lastName = form.cleaned_data['last_name']
            # Create the User record
            user = User.objects.create_user(username, email, password)
            user.save()
            # Auto login the user
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # A backend authenticated the credentials
                login(request, user)
                return HttpResponseRedirect('/preferences/')
            else:
                return HttpResponseRedirect('/')
>>>>>>> 46cc6393178aef68c61606c7e4d25c362dcdb201
        else:
            HttpResponseRedirect(self.url)
