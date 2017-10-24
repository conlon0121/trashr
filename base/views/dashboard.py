from django.shortcuts import render
from django.views.generic import View
from base.forms import DumpsterFilterForm, DumpsterSelectForm
from base.tables import DumpsterTable
from django_tables2 import RequestConfig
from base.models import Dumpster


class DashboardView(View):
    template_name = "logged_in/dashboard.html"
    form_class_filter = DumpsterFilterForm
    form_class_select = DumpsterSelectForm

    def get(self, request):
        table = DumpsterTable(Dumpster.objects.all())
        form_filter = self.form_class_filter()
        form_select = self.form_class_select()
        return render(request, self.template_name, {'table': table,
                                                    'form_filter': form_filter,
                                                    'form_select': form_select})

    def post(self, request):
        form = self.form_class_filter(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            percent_fill = -1
            dumpster_filter = Dumpster.objects.all()
            operator = None
            if data['address']:
                dumpster_filter = Dumpster.objects.filter(address__icontains=data['address'])
            if data['location']:
                dumpster_filter = dumpster_filter.filter(location__icontains=data['location'])
            if data['utility']:
                dumpster_filter = dumpster_filter.filter(utility=data['utility'])
            if data['percent_fill']:
                percent_fill = int(data['percent_fill'])
                operator = int(data['operator'])
                if operator == -1:
                    for dumpster in dumpster_filter:
                        if dumpster.percent_fill >= percent_fill:
                            dumpster_filter = dumpster_filter.exclude(pk=dumpster.pk)
                if operator == 0:
                    for dumpster in dumpster_filter:
                        if dumpster.percent_fill != percent_fill:
                            dumpster_filter = dumpster_filter.exclude(pk=dumpster.pk)
                if operator == 1:
                    for dumpster in dumpster_filter:
                        if dumpster.percent_fill <= percent_fill:
                            dumpster_filter = dumpster_filter.exclude(pk=dumpster.pk)
            table = DumpsterTable(dumpster_filter)
            return render(request, 'table.html', {'table': table})
