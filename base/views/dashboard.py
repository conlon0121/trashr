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
            features.append({
                "type": "Point",
                "properties": {
                    "description": float(dumpster.percent_fill),
                    "icon": "theatre"
                },
                "geometry": {
                    "type": "point",
                    "coordinates": [float(dumpster.longitude), float(dumpster.latitude)]
                }
            })
        layer = {
            "id": "dumpsters",
            "type": "symbol",
            "source": {
                "type": "geojson",
                "data": {
                    "type": "FeatureCollection",
                    "features": features
                }
            },
            "layout": {
                "icon-image": "{icon}-15",
                "icon-allow-overlap": True
            }
        }
        table = DumpsterTable(dumpsters)
        form_filter = self.form_class_filter()
        form_select = self.form_class_select()
        return render(request, self.template_name, {'table': table,
                                                    'form_filter': form_filter,
                                                    'form_select': form_select,
                                                    'layer': json.dumps(layer)})
