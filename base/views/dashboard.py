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

    @staticmethod
    def post(request):
        data = dict(request.POST)
        percent_fill = -1
        dumpster_filter = Dumpster.objects.all()
        operator = None
        import pdb; pdb.set_trace()
        if data['address'][0]:
            dumpster_filter = Dumpster.objects.filter(address=data['address'])
        if data['location'][0]:
            dumpster_filter = dumpster_filter.filter(location=data['location'])
        if data['utility'][0]:
            dumpster_filter = dumpster_filter.filter(utility=data['utility'])
        if data['percent_fill'][0]:
            percent_fill = int(data['percent_fill'][0])
            operator = data['operator'][0]
            if int(operator) == -1:
                for dumpster in dumpster_filter:
                    if dumpster.percent_fill >= percent_fill:
                        dumpster_filter.exclude(pk=dumpster.pk)
            if int(operator) == 0:
                for dumpster in dumpster_filter:
                    if dumpster.percent_fill == percent_fill:
                        dumpster_filter.exclude(pk=dumpster.pk)
            if int(operator) == 1:
                for dumpster in dumpster_filter:
                    if dumpster.percent_fill <= percent_fill:
                        dumpster_filter.exclude(pk=dumpster.pk)
        table = DumpsterTable(dumpster_filter)
        RequestConfig(request, paginate={"per_page": 10}).configure(table)
        return render(request, {'table': table})
