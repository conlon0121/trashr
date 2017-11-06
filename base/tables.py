from django.utils.html import escape
from django.utils.safestring import mark_safe
from django_tables2 import Table, Column, DateTimeColumn, TemplateColumn
from base.models import Dumpster, Route


class DumpsterTable(Table):
    # pylint: disable=no-init
    date = DateTimeColumn(orderable=False, accessor='last_updated', verbose_name='Last Updated')
    address = Column(accessor='address', orderable=False, verbose_name='Dumpster')
    util = Column(accessor='get_utility', verbose_name='Utility')
    container_type = Column(accessor='container_type', verbose_name='Type')
    fill_percentage = TemplateColumn(
        '{% with fill=record.percent_fill %}'
          '{% if not fill %}<p style="color:green">0%</p>'
          '{% elif fill < 30 %}'
            '<p style="color:green">{{fill}}%</p>'
          '{% elif fill > 50 %}'
            '<p style="color:red">{{fill}}%</p>'
          '{% else %}'
            '<p style="color:#FFA500">{{fill}}%</p>'
          '{% endif %}'
        '{% endwith %}',
            accessor='percent_fill',
            verbose_name='% Fill'
            )

    class Meta:
        model = Dumpster
        sequence = ('address', 'util', 'date', 'fill_percentage')
        exclude = ('utility', 'container_type', 'id', 'org', 'location', 'rfid', 'capacity',
                   'capacity_units', 'latitude', 'longitude', 'functioning', 'percent_fill', 'last_updated')
        template = 'table.html'

class DeleteColumn(Column):
    empty_values = list()
    def render(self, value, record):
        return mark_safe('<button id="%s" class="btn btn-danger">Delete Route</button>' % escape(record.id))


class RouteTable(Table):
    delete = DeleteColumn()

    class Meta:
        model = Route
        sequence = ('number_of_dumpsters', 'time_estimate', 'driver', 'delete')
        exclude = ('date', 'id',)
        template = 'route_table.html'
