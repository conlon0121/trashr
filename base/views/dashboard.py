import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import View
from base.forms import DumpsterUpdateForm
from base.tables import DumpsterTable
from base.models import Dumpster
from base.views.utils import get_layer


@method_decorator(login_required, name='dispatch')
class DashboardView(View):
    template_name = "logged_in/dashboard.html"
    form_class = DumpsterUpdateForm

    def get(self, request):
        dumpsters = Dumpster.objects.all()
        layer, lat, long = get_layer(dumpsters)
        table = DumpsterTable(dumpsters)
        return render(request, self.template_name, {'table': table,
                                                    'form_update': self.form_class(),
                                                    'lat': lat,
                                                    'long': long,
                                                    'layer': json.dumps(layer),
                                                    })

class AlertUpdateView(View):
    form_class = DumpsterUpdateForm

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form_vals = form.cleaned_data
            Dumpster.objects.filter(id=form_vals['dumpster']).update(alert_percentage=form_vals['percentage'])
            return JsonResponse({"success": 1})
        else:
            return JsonResponse({"success": 0})

