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
