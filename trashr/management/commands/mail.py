from django.core.mail import send_mail
from django.core.management.base import BaseCommand



class Command(BaseCommand):
    help = "Creates events based on the NC state calendar"

    def handle(self, *args, **options):
        send_mail(
            'test',
            'test',
            'trashrwaste@gmail.com',
            ['conlon0121@gmail.com'],
            fail_silently=False,
            )