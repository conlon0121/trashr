from django_tables2 import Table, Column, DateTimeColumn, TemplateColumn, CheckBoxColumn
from base.models import Dumpster


class DumpsterTable(Table):
    # pylint: disable=no-init
    date = DateTimeColumn(orderable=False, accessor='last_updated', verbose_name='Last Updated')
    address = Column(accessor='address', orderable=False, verbose_name='Dumpster')
    util = Column(accessor='get_utility', verbose_name='Utility')
    container_type = Column(accessor='container_type', verbose_name='Type')
    fill_percentage = TemplateColumn(
            '{% if not record.percent_fill %}<p style="color:green">0%</p>{% elif record.percent_fill < 30 %}<p style="color:green">{{record.percent_fill}}%</p>{% elif record.percent_fill > 50 %}<p style="color:yellow"></p>{% else %}<p style="color:red"></p>{% endif %}',
            accessor='percent_fill',
            verbose_name='% Fill'
            )

    class Meta:
        model = Dumpster
        sequence = ('address', 'util', 'date', 'fill_percentage')
        exclude = ('utility', 'container_type', 'id', 'org', 'location', 'rfid', 'capacity', 'capacity_units', 'latitude', 'longitude', 'functioning')
        template = 'table.html'
