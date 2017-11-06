import ast
import json

from django.shortcuts import render
from django.views.generic import View

from base.forms import DumpsterSelectForm
from base.models import Dumpster, Route
from base.tables import RouteTable


class RouteView(View):
    template_name = "logged_in/route.html"
    form_class_select = DumpsterSelectForm

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        import pdb; pdb.set_trace()
        dumpster_ids = ast.literal_eval(dict(request.POST)['dumpsters'][0])
        dumpsters = Dumpster.objects.filter(id__in=dumpster_ids)
        features = []
        lat_longs = ''
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
                                   f'<center>{str(fill)}% full</center>',
                    "marker-color": color,
                    "marker-size": "small",
                    "marker-symbol": f'{str(dumpster.percent_fill)}'
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [d_long, d_lat]
                }
            })
            lat_longs += str(dumpster.latitude) + ',' + str(dumpster.longitude) + ';'

        table = RouteTable([Route(time_estimate=30, number_of_dumpsters=dumpsters.count())])
        lat_longs = lat_longs[:-1]
        try:
            lat = lat / len(features)
            long = long / len(features)
        except ZeroDivisionError:
            pass
        return render(request, self.template_name, {'table': table,
                                                    'layer': json.dumps(features),
                                                    'lat_longs': lat_longs,
                                                    'lat': lat,
                                                    'long': long,
                                                    })
