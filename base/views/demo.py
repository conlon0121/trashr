from django.shortcuts import render
from django.utils import timezone
from django.views.generic import View
from base.models import Dumpster, IntervalReading, IntervalSet


class DemoView(View):
    template_name = "old_index.html"

    def get(self, request):
        # Get the percent capacity of the latest interval reading for the input dumpster
        current_hour = timezone.localtime(timezone.now()).hour
        if current_hour >= 17:
            greeting = "Good Evening, Lani"
        elif current_hour > 12:
            greeting = "Good Afternoon, Lani"
        else:
            greeting = "Good Morning, Lani"
        done = False
        # Try at most 5 times to get a good reading
        try:
            for int_set in IntervalSet.objects.filter(dumpster__id=1).order_by('-timestamp'):
                timestamp = timezone.localtime(int_set.timestamp)
                try:
                    reading = int_set.intervalreading_set.get(angle=18)
                    percent_fill = int(reading.percent_fill) - (int(reading.percent_fill) % 5)
                    break
                except IntervalReading.DoesNotExist:
                    continue
        except IntervalSet.DoesNotExist:
            percent_fill = 0
            timestamp = None
        return render(request, self.template_name, {'percent_fill': percent_fill, 'greeting': greeting, 'timestamp': timestamp})

