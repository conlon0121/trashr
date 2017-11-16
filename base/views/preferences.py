from django.shortcuts import render_to_response
from django.views.generic import View
import json

from django.shortcuts import render


class PreferencesView(View):
    template_name = "logged_in/preferences.html"

    def get(self, request):
        return render_to_response(self.template_name)

    def post(self, request):
        dict(request.POST)
