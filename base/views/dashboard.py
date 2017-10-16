from django.shortcuts import render
from django.views.generic import View
from base.forms import DumpsterFilterForm
from base.tables import DumpsterTable
from django_tables2 import RequestConfig
from base.models import Dumpster


class DashboardView(View):
    template_name = "logged_in/dashboard.html"
    form_class = DumpsterFilterForm

    def get(self, request):
        table = DumpsterTable(Dumpster.objects.all())
        form = self.form_class()
        RequestConfig(request, paginate={"per_page": 10}).configure(table)
        return render(request, self.template_name, {'table': table, 'form': form})

class DumpsterFilterTable(View):
    template_name = "table.html"

    def post(self, request):
        data = dict(request.POST)
        percent_fill = -1
        dumpster_filter = Dumpster.objects.all()
        operator = None
        if data['address'][0]:
            dumpster_filter = Dumpster.objects.filter(address__icontains=data['address'][0])
        if data['location'][0]:
            dumpster_filter = dumpster_filter.filter(location__icontains=data['location'][0])
        if data['utility'][0]:
            dumpster_filter = dumpster_filter.filter(utility=data['utility'][0])
        if data['percent_fill'][0]:
            percent_fill = int(data['percent_fill'][0])
            operator = int(data['operator'][0])
            if operator == -1:
                for dumpster in dumpster_filter:
                    if dumpster.percent_fill >= percent_fill:
                        dumpster_filter = dumpster_filter.exclude(pk=dumpster.pk)
            import pdb; pdb.set_trace()
            if operator == 0:
                for dumpster in dumpster_filter:
                    if dumpster.percent_fill != percent_fill:
                        dumpster_filter = dumpster_filter.exclude(pk=dumpster.pk)
            if operator == 1:
                for dumpster in dumpster_filter:
                    if dumpster.percent_fill <= percent_fill:
                        dumpster_filter = dumpster_filter.exclude(pk=dumpster.pk)
        table = DumpsterTable(dumpster_filter)
        RequestConfig(request, paginate={"per_page": 10}).configure(table)
        return render(request, self.template_name, {'table': table})
