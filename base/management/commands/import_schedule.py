from django.core.management.base import BaseCommand
from lxml import html
import requests


class Command(BaseCommand):
    help = "Creates events based on the NC state calendar"

    def handle(self, *args, **options):
        page = requests.get('http://calendar.activedatax.com/ncstate/EventList.aspx')
        tree = html.fromstring(page.content)
        event_dates = tree.xpath('//table[@id="tblHighlight"]//span[@class="listheadtext"]/text()')
        event_times = tree.xpath('//table[@id="tblHighlight"]//a[@class="listtext"]/text()')
        event_names = tree.xpath('//table[@id="tblHighlight"]//a[@class="url"]/text()')
