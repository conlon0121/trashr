from datetime import timedelta

from dal import autocomplete
from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.http import JsonResponse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import View

from django.shortcuts import render

from trashr.forms import EmailForm, EmailNotificationForm
from trashr.models import UserProfile, Alert, Email


@method_decorator(login_required, name='dispatch')
class PreferencesView(View):
    template_name = "logged_in/preferences.html"
    form_class_add = EmailNotificationForm
    form_class_verify = EmailForm

    def get(self, request):
        company = UserProfile.objects.get(user=request.user).org
        emails = Email.objects.filter(org=company, receives_alerts=True)
        alerts = Alert.objects.filter(timestamp__gte=timezone.now() - timedelta(days=30),
                                      dumpster__org=company).prefetch_related('dumpster')\
            .annotate(current_fill=F('dumpster__percent_fill'), address=F('dumpster__address'))
        return render(request, self.template_name, {'name': company.name,
                                                    'code': company.code,
                                                    'email': request.user.email,
                                                    'emails': emails,
                                                    'alerts': alerts,
                                                    'form': self.form_class_add(),
                                                    'form_verify': self.form_class_verify(),
                                                    })

    def post(self, request):
        form = self.form_class_add(request.POST)
        if form.is_valid():
            form_vals = form.cleaned_data
            email = form_vals['email_add']
            try:
                email_obj = Email.objects.get(email=email)
                org = UserProfile.objects.get(user=request.user).org
                if email_obj.org != org:
                    return JsonResponse({'message': 'Invalid email address'}, status=400)
                if email_obj.receives_alerts:
                    return JsonResponse({"message": "Email address already receives alerts"}, status=400)
                email_obj.receives_alerts = True
                email_obj.save()
            except Email.DoesNotExist():
                return JsonResponse({'message': 'Email address does not exist'}, status=400)
            return JsonResponse({'email': email}, status=200)
        return JsonResponse({'message': 'Invalid email address, you may need to refresh the page.'}, status=400)


@method_decorator(login_required, name='dispatch')
class EmailDelete(View):
    form_class = EmailForm

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            Email.objects.filter(email=form.cleaned_data['email']).update(receives_alerts=False)
            return JsonResponse({'email': form.cleaned_data['email']}, status=200)
        return JsonResponse({'message': 'Something went wrong'}, status=400)


@method_decorator(login_required, name='dispatch')
class EmailAutoComplete(autocomplete.Select2ListView):
    def get_list(self):
        org = UserProfile.objects.get(user=self.request.user).org
        return Email.objects.filter(org=org, receives_alerts=False).values_list('email', flat=True)
