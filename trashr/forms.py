from django import forms
from django.contrib.auth.forms import UserCreationForm


class DumpsterUpdateForm(forms.Form):
    dumpster = forms.IntegerField(required=True)
    percentage = forms.IntegerField(required=True)


class AccountForm(UserCreationForm):
    password1 = forms.CharField(required=True, widget=forms.PasswordInput())
    password2 = forms.CharField(required=True, widget=forms.PasswordInput())
    company_code = forms.CharField(required=True)


class PrefsForm(forms.Form):
    pass


class ResetForm(forms.Form):
    password1 = forms.CharField(required=True, widget=forms.PasswordInput())
    password2 = forms.CharField(required=True, widget=forms.PasswordInput())


class ResetRequestForm(forms.Form):
    email = forms.EmailField(required=True)
