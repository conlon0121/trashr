from django import forms


class DumpsterSelectForm(forms.Form):
    dumpsters = forms.CharField(required=True)
