from django import forms


class DumpsterFilterForm(forms.Form):
    address = forms.CharField(max_length=50,
                              required=False,
                              )
    location = forms.CharField(max_length=50,
                              required=False,
                              )
    percent_fill = forms.IntegerField(required=False, label="% Fill")
    operator = forms.ChoiceField(required=False,
                                 choices=[(1, 'Greater than'), (-1, 'Less than'), (0, 'Equal to')],
                                 initial='1',
                                 )
    utility = forms.ChoiceField(required=False,
                                choices=[('', ''), (0, 'Trash'), (1, 'Recycling')],
                                )

    def clean(self):
        cd = super(DumpsterFilterForm, self).clean()

        if self.data.get('percent_fill'):
            percent_fill = self.data.get('percent_fill')
            if percent_fill > 100 or percent_fill < 0:
                raise forms.ValidationError('Please enter a fill percentage between 0 and 100.')
