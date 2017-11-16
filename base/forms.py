from django import forms
from django.contrib.auth.forms import UserCreationForm


class DumpsterSelectForm(forms.Form):
    dumpsters = forms.CharField(required=True)





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
