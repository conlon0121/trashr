from dal import autocomplete
from django import forms
from django.contrib.auth.forms import UserCreationForm

from trashr.models import Email, Organization


class DumpsterUpdateForm(forms.Form):
    dumpster = forms.IntegerField(required=True)
    percentage = forms.IntegerField(required=True)


class AccountForm(UserCreationForm):
    password1 = forms.CharField(required=True, widget=forms.PasswordInput())
    password2 = forms.CharField(required=True, widget=forms.PasswordInput())
    company_code = forms.CharField(required=True)

    def clean(self):
        cleaned_data = super().clean()
        try:
            email = Email.objects.get(email=cleaned_data['username'])
            org = Organization.objects.get(code=cleaned_data['company_code'])
            if email.org != org:
                return forms.ValidationError("This email address is already registered to another organization.")
        except (Email.DoesNotExist, Organization.DoesNotExist):
            pass

    def clean_company_code(self):
        data = self.cleaned_data['company_code']
        if data == 'demo':
            raise forms.ValidationError("Creating demo users is not allowed.")
        return data


class PrefsForm(forms.Form):
    pass


class ResetForm(forms.Form):
    password1 = forms.CharField(required=True, widget=forms.PasswordInput())
    password2 = forms.CharField(required=True, widget=forms.PasswordInput())


class EmailForm(forms.Form):
    email = forms.EmailField(required=True)


class EmailNotificationForm(forms.Form):
    email_add = autocomplete.Select2ListChoiceField(
        widget=autocomplete.ListSelect2(url='email-autocomplete'),
        choice_list=list(Email.objects.all().values_list('email', flat=True)))
