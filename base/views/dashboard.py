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
        lat = 0
        long = 0
        for dumpster in dumpsters:
            fill = dumpster.percent_fill
            d_lat = float(dumpster.latitude)
            d_long = float(dumpster.longitude)
            lat += d_lat
            long += d_long
            if fill < 30:
                color = "#00a600"
            elif fill > 50:
                color = "#ec0000"
            else:
                color = "#eca01e"
            features.append({
                "type": "Feature",
                "properties": {
                    "description": f'{dumpster.address}<br/>'
                                   f'<center>{str(dumpster.percent_fill)}% full</center>'
                                   f'<button id={str(dumpster.id)}>select in table</button>',
                    "marker-color": color,
                    "marker-size": "small",
                    "marker-symbol": f'{str(dumpster.percent_fill)}'
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [d_long, d_lat]
                }
            })
        try:
            lat = lat / len(features)
            long = long / len(features)
        except ZeroDivisionError:
            pass
        table = DumpsterTable(dumpsters)
        form_filter = self.form_class_filter()
        form_select = self.form_class_select()
        return render(request, self.template_name, {'table': table,
                                                    'form_filter': form_filter,
                                                    'form_select': form_select,
                                                    'lat': lat,
                                                    'long': long,
                                                    'layer': json.dumps(features)})

class RouteMaker(View):

    def post(self, request):
        import pdb; pdb.set_trace()
        data = request.POST