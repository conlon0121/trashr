import json

from django.shortcuts import render_to_response
from django.views.generic import View


class GraphView(View):
    template_name = "logged_in/maps.html"


    def get(self, request):
        return render_to_response(self.template_name)

    def post(self, request):
        import pdb; pdb.set_trace()

        dumpster_ids = json.loads(dict(request.POST)['dumpsters'][0])

