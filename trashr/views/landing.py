from django.shortcuts import render
from django.views.generic import View


class IndexView(View):
    template_name = "landing/index.html"

    def get(self, request):
        return render(request, self.template_name)


class ServicesView(View):
    template_name = "landing/services.html"

    def get(self, request):
        return render(request, self.template_name)


class TechnologyView(View):
    template_name = "landing/technology.html"

    def get(self, request):
        return render(request, self.template_name)


class TermsView(View):
    template_name = "landing/tac.html"

    def get(self, request):
        return render(request, self.template_name)


class PrivacyView(View):
    template_name = "landing/privacy.html"

    def get(self, request):
        return render(request, self.template_name)


class AboutView(View):
    template_name = "landing/about.html"

    def get(self, request):
        return render(request, self.template_name)


class ContactView(View):
    template_name = "landing/contact.html"

    def get(self, request):
        return render(request, self.template_name)