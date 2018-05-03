import csv
import os
from datetime import timedelta
from decimal import Decimal
from random import randint, getrandbits

from django.conf import settings
from django.core.management import BaseCommand
from django.utils import timezone

from trashr.models import *


class Command(BaseCommand):
    help = 'Add a demo user to the database with demo data'

    def handle(self, *args, **options):
        # Load in NC State test dumpster file
        org, _ = Organization.objects.update_or_create(name="Demo", code="trashrdemo")
        Dumpster.objects.filter(org=org).delete()
        filepath = os.path.join(settings.BASE_DIR, 'trashr/dumpter_files/test_dumpsters.csv')
        with open(filepath, 'r', encoding='latin-1') as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader)
            for row in csv_reader:
                alert = randint(55, 85)
                d = Dumpster.objects.create(
                    org=org,
                    location=row[0],
                    address=row[3] + ' ' + row[4],
                    coordinates=[Decimal(row[5]), Decimal(row[6])],
                    rfid=row[7],
                    capacity=row[8],
                    capacity_units=row[9],
                    container_type=row[11],
                    percent_fill=randint(20, 85),
                    alert_percentage=alert,
                )
                if getrandbits(1):
                    Alert.objects.create(dumpster=d, fill_percent=randint(alert, alert + 15),
                                         timestamp=timezone.now() - timedelta(days=randint(1, 30)))

        Email.objects.update_or_create(email='nick.conlon@trashr.io', org=org)
        Email.objects.update_or_create(email='nick@trashr.io', org=org)
        Email.objects.update_or_create(email='goutham@trashr.io', org=org)
        Email.objects.update_or_create(email='hartley@trashr.io', org=org)
