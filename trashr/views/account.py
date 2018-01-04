from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.shortcuts import render, render_to_response
from django.views.generic import View
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login

from trashr.forms import AccountForm
from trashr.models import Organization, UserProfile


class AccountView(View):
    template_name = 'registration/account.html'
    form_class = AccountForm
    url = '/signup/$'
    
    def get(self, request):
        return render(request, self.template_name, {'form':AccountForm()})


    def post(self, request):
        form = AccountForm(request.POST)
        if form.is_valid():
            # Unpack form values
            email = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            company_code = form.cleaned_data['company_code']
            try:
                validate_email(email)
            except ValidationError:
                messages.error(request, 'Invalid email address')
                return render(request, self.template_name, {'form': form})
            try:
                org = Organization.objects.get(code=company_code)
            except Organization.DoesNotExist:
                messages.error(request, 'Invalid company code')
                return render(request, self.template_name, {'form': form})
            # Create the User record
            user = User.objects.create_user(email, email, password)
            UserProfile.objects.create(user=user, org=org)
            # Auto login the user
            user = authenticate(request, username=email, password=password)
            if user is not None:
                # A backend authenticated the credentials
                login(request, user)
                return HttpResponseRedirect('/accounts/accountSuccess')
        for field, err_list in form.errors.items():
            for err in err_list:
                messages.error(request, err)
        return render(request, self.template_name, {'form': form})


class AccountSuccessView(View):
    template_name = 'registration/accountSuccess.html'
    url = '/accounts/accountSuccess/'

    def get(self, request):
        return render_to_response(self.template_name)


