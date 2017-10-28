from django.shortcuts import render_to_response
from django.views.generic import View


class MapView(View):
    template_name = "logged_in/maps.html"

    def get(self, request):
        return render_to_response(self.template_name)

    def post(self, request):
        dict(request.POST)
