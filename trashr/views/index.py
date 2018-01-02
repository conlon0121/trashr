from django.shortcuts import render
from django.views.generic import View


class IndexView(View):
    #TODO:Change to index when functional
    template_name = "index.html"

    def get(self, request):
        return render(request, self.template_name)

