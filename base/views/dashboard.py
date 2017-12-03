import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import View
from base.forms import DumpsterSelectForm
from base.tables import DumpsterTable
from base.models import Dumpster
from base.views.utils import get_layer


@method_decorator(login_required, name='dispatch')
class DashboardView(View):
    template_name = "logged_in/dashboard.html"
    form_class_select = DumpsterSelectForm

    def get(self, request):
        dumpsters = Dumpster.objects.all()
        layer, lat, long = get_layer(dumpsters)
        table = DumpsterTable(dumpsters)
        form_select = self.form_class_select()
        return render(request, self.template_name, {'table': table,
                                                    'form_select': form_select,
                                                    'lat': lat,
                                                    'long': long,
                                                    'layer': json.dumps(layer),
                                                    })
