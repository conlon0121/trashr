from django.shortcuts import render
from django.views.generic import View


class PrivacyView(View):
    #TODO:Change to index when functional
    template_name = "privacy.html"

    def get(self, request):
        return render(request, self.template_name)
