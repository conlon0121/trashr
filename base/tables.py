from django_tables2 import Table, Column, DateTimeColumn, TemplateColumn
from base.models import Dumpster


class DumpsterTable(Table):
    # pylint: disable=no-init
    date = DateTimeColumn(orderable=False, accessor='last_updated', verbose_name='Last Updated')
    address = Column(accessor='address', orderable=False, verbose_name='Dumpster')
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
    alert_percentage = TemplateColumn(
        '<input class="update-input"'
        ' style="width:70%; box-shadow: 0 0 0px #58ca7e;"'
        ' data="{{record.coordinates}}"'
        ' type="number"'
        ' value={{record.alert_percentage}}>'
        '</input>',
        accessor='alert_percentage',
        verbose_name='Alert %',
        attrs={"th": {'style': "width:13%"},
               "td": {'style': "width:13%"}})

    class Meta:
        model = Dumpster
        sequence = ('address', 'date', 'fill_percentage', 'alert_percentage')
        exclude = ('alert_sent', 'utility', 'container_type', 'id', 'org', 'location', 'rfid', 'capacity',
                   'capacity_units', 'coordinates', 'functioning', 'percent_fill', 'last_updated')
        template = 'table.html'
