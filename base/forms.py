from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone


class DumpsterSelectForm(forms.Form):
    dumpsters = forms.CharField(required=True)
    drivers = forms.CharField(required=True)


class AccountForm(UserCreationForm):
    username = forms.CharField(
       required=True, widget=forms.TextInput(attrs={'class':'form-control'})
    )
##    first_names = forms.CharField(
##        required=True,widget=forms.TextInput(attrs={'class':'form-control'})
##    )
##    last_names = forms.CharField(
##        required=True, widget=forms.TextInput(attrs={'class':'form-control'})
##    )
##    email = forms.CharField(
##        required=True, widget=forms.TextInput(attrs={'class':'form-control'})
##    )
    password1 = forms.CharField(
        required=True, widget=forms.TextInput(attrs={'class':'form-control', 'type':'password'})
    )
    password2 = forms.CharField(
        required=True, widget=forms.TextInput(attrs={'class':'form-control', 'type':'password'})
    )

class CompanyCodeForm(forms.Form):
    companyCode = forms.CharField(
       required=False, widget=forms.TextInput(attrs={'class':'form-control'})
    )


class RouteDateForm(forms.Form):
    date = forms.DateField(initial=timezone.localtime().date())
