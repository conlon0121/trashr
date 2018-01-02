import csv
import os
from _decimal import Decimal

from django.conf import settings
from django.core.management.base import BaseCommand

from trashr.models import Organization, Dumpster


class Command(BaseCommand):
    help = "imports a csv file via relative pathname"

    @staticmethod
    def add_arguments(parser):
        parser.add_argument(
            '-f',
            metavar='<filename>',
            help='path of the file from root of the project'
        )

    def handle(self, *args, **options):
        ncsu = Organization.objects.filter(name='ncsu')
        if not ncsu.exists():
            ncsu = Organization.objects.create(name="ncsu")
        else:
            ncsu = ncsu.get()
        filepath = options.get('f')
        filepath = os.path.join(settings.BASE_DIR, filepath)
        with open(filepath, 'r', encoding='latin-1') as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader)
            for row in csv_reader:
                Dumpster.objects.create(
                    org=ncsu,
                    location=row[0],
                    address=row[3] + ' ' + row[4],
                    coordinates=[Decimal(row[5]), Decimal(row[6])],
                    rfid=row[7],
                    capacity=row[8],
                    capacity_units=row[9],
                    container_type=row[11],
                )
