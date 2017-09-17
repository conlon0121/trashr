import os
import subprocess
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Compiles SCSS files to CSS with compass'

    def handle(self, *args, **options):
    # Go to the same folder as config.rb
    os.chdir('base/static/')
    # Run compass
    subprocess.run(['compass', 'compile', 'sass/all.scss'])
    subprocess.run(['compass', 'compile', 'sass/admin.scss'])

