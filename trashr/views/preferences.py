from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import View
import json

from django.shortcuts import render

from trashr.models import Organization, UserProfile


@method_decorator(login_required, name='dispatch')
class PreferencesView(View):
    template_name = "logged_in/preferences.html"

    def get(self, request):
        # TODO: Make sure users have userprofiles and companies
        company = UserProfile.objects.get(user=request.user).org
        return render(request, self.template_name, {'name': company.name,
                                                    'code': company.code,
                                                    'email': request.user.email})

    def post(self, request):
        dict(request.POST)
