from django.shortcuts import render
from django.utils import timezone
from django.views.generic import View
from trashr.models import Dumpster, IntervalReading


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
            dumpster = Dumpster.objects.get(id=1)
            percent_fill = dumpster.percent_fill
            timestamp = IntervalReading.objects.filter(dumpster=dumpster).latest('timestamp').timestamp

        except Dumpster.DoesNotExist:
            percent_fill = 0
        except IntervalReading.DoesNotExist:
            timestamp = None

            timestamp = None
        return render(request, self.template_name, {'percent_fill': percent_fill, 'greeting': greeting, 'timestamp': timestamp})

