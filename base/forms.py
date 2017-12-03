from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone


class DumpsterSelectForm(forms.Form):
    dumpsters = forms.CharField(required=True)
    drivers = forms.CharField(required=True)


class AccountForm(UserCreationForm):
    #email = forms.EmailField(
    #   required=True, widget=forms.TextInput(attrs={'class':'form-control'})
    #)
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class':'form-control'})
    )
    password1 = forms.CharField(
        widget=forms.TextInput(attrs={'class':'form-control', 'type':'password'})
    )
    password2 = forms.CharField(
        widget=forms.TextInput(attrs={'class':'form-control', 'type':'password'})
    )


class RouteDateForm(forms.Form):
    date = forms.DateField(initial=timezone.localtime().date())
