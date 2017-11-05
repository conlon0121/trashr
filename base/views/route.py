import json

from django.shortcuts import render
from django.views.generic import View

from base.forms import DumpsterSelectForm
from base.models import Dumpster
from base.tables import DumpsterTable


class RouteView(View):
    template_name = "logged_in/route.html"
    form_class_select = DumpsterSelectForm

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        dumpster_ids = json.loads(dict(request.POST)['dumpsters'][0])
        dumpsters = Dumpster.objects.filter(id__in=dumpster_ids)
        features = []
        lat_longs = ''
        for dumpster in dumpsters:
            features.append({
                "type": "Feature",
                "properties": {
                    "description": f'{dumpster.address}<br/>'
                                   f'<center>{str(dumpster.percent_fill)}% full</center>',
                    "icon": "circle",
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [dumpster.longitude, dumpster.latitude]
                }
            })

        lat_longs += str(dumpster.latitude) + ',' + str(dumpster.longitude) + ';'
        table = DumpsterTable(dumpsters)
        lat_longs = lat_longs[:-1]

        import pdb; pdb.set_trace()


        return render(request, self.template_name, {'table': table,
                                                    'layer': json.dumps(features),
                                                    'lat_longs': lat_longs})
