from django.shortcust import render_to_response
from django.views.generic import View


class IndexView(View):
    #TODO:Change to index when functional
    template_name = "index.html"

    def get(self, request):
        return render_to_response(self.template_name)

