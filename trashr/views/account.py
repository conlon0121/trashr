from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.shortcuts import render, render_to_response, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import View
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six

from trashr.forms import AccountForm, ResetForm, ResetRequestForm
from trashr.models import Organization, UserProfile


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.is_active)
        )
account_activation_token = TokenGenerator()


class AccountView(View):
    template_name = 'registration/account.html'
    form_class = AccountForm
    url = '/signup/$'

    def get(self, request):
        return render(request, self.template_name, {'form':AccountForm()})


    def post(self, request):
        form = AccountForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            company_code = form.cleaned_data['company_code']
            try:
                validate_email(email)
            except ValidationError:
                messages.error(request, 'Invalid email address')
                return render(request, self.template_name, {'form': form})
            try:
                org = Organization.objects.get(code__iexact=company_code)
            except Organization.DoesNotExist:
                messages.error(request, 'Invalid company code')
                return render(request, self.template_name, {'form': form})
            user = User.objects.create_user(email, email, password)
            UserProfile.objects.create(user=user, org=org)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            message = render_to_string('registration/email.html', {
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            send_mail(
                'Please Verify Your Email',
                message,
                'trashrwaste@gmail.com',
                [email]
            )
            return render(request, 'registration/account_info.html',
                          {'info': 'Thanks for signing up! '
                                   'Please confirm your email address to complete the registration'})
        for field, err_list in form.errors.items():
            for err in err_list:
                messages.error(request, err)
        return render(request, self.template_name, {'form': form})


class ActivateAccount(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return render(request, 'registration/account_success.html')
        else:
            return render(request, 'registration/account_info.html', {'info': 'Activation link is invalid!'})


class ResetPasswordRequest(View):
    form_class = ResetRequestForm
    template_name = 'registration/password_reset_form.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        form = ResetForm(request.POST)
        if form.is_valid() and request.user.email == form['email']:
            current_site = get_current_site(request)
            message = render_to_string('registration/password_reset_email.html', {
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(request.user.pk)),
                'token': account_activation_token.make_token(request.user),
            })
            send_mail(
                'Please Verify Your Email',
                message,
                'trashrwaste@gmail.com',
                [UserProfile.objects.get(user=request.user).email]
            )
            return render(request, 'registration/password_reset_done.html')
        return render(request, self.template_name, {'form': form})


class ResetConfirm(View):
    form_class = ResetForm
    template_name = 'registration/password_reset_confirm.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        form = ResetForm(request.POST)
        if form.is_valid() and form['password1'] == form['password2']:
            request.user.set_password(form['password1'])
            return render(request, 'registration/password_reset_complete.html')
        return render(request, self.template_name, {'form': form})


class SuccessView(View):
    template_name = 'registration/success.html'
    url = '/accounts/success/'

    def get(self, request):
        return render_to_response(self.template_name)
