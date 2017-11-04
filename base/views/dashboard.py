import json

from django.shortcuts import render
from django.views.generic import View
from base.forms import DumpsterFilterForm, DumpsterSelectForm
from base.tables import DumpsterTable
from base.models import Dumpster


class DashboardView(View):
    template_name = "logged_in/dashboard.html"
    form_class_filter = DumpsterFilterForm
    form_class_select = DumpsterSelectForm

    def get(self, request):
        dumpsters = Dumpster.objects.all()
        features = []
        for dumpster in dumpsters:
            fill = dumpster.percent_fill
            if fill < 30:
                color = "#00a600"
            elif fill > 50:
                color = "#ec0000"
            else:
                color = "#eca01e"
            features.append({
                "type": "Feature",
                "properties": {
                    "description": str(dumpster.percent_fill),
                    "marker-color": color,
                    "marker-size": "small"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [float(dumpster.longitude), float(dumpster.latitude)]
                }
            })
        table = DumpsterTable(dumpsters)
        form_filter = self.form_class_filter()
        form_select = self.form_class_select()
        return render(request, self.template_name, {'table': table,
                                                    'form_filter': form_filter,
                                                    'form_select': form_select,
                                                    'layer': json.dumps(features)})
