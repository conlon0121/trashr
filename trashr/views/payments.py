import datetime, time

import stripe
from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import reverse, render
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import View

from trashr.forms import PaymentForm
from trashr.models import PaymentMethod, UserProfile, Subscription, Plan, Product, Dumpster, Transaction


@method_decorator(login_required, name='dispatch')
class PaymentUpdate(View):

    @staticmethod
    def post(request):
        if UserProfile.objects.get(user=request.user).org.name == 'Demo':
            return HttpResponseRedirect(reverse('preferences'))
        form = PaymentForm(request.POST)
        if form.is_valid():
            try:
                stripe.api_key = settings.STRIPE_SECRET_KEY

                method = PaymentMethod.objects.get(profile__user=request.user)
                customer = stripe.Customer.retrieve(method.customer_id)
                customer.source = form.cleaned_data['stripeToken']

                data = customer.save()['sources']['data'][0]

                method.card_id = data['id']
                method.last_four_digits = data['last4']
                method.card_type = data['brand']
                method.expires = datetime.date(day=1,
                                               month=data['exp_month'],
                                               year=data['exp_year'])
                method.save()
            except Exception:
                # Either there was no 'method_id' or we couldn't find a PaymentMethod with that id
                return HttpResponseRedirect(reverse('preferences'))
            return HttpResponseRedirect(reverse('preferences'))


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(lambda u: not UserProfile.objects.get(user=u).org.active,
                                   login_url='/checkout/'), name='get')
@method_decorator(user_passes_test(lambda u: not UserProfile.objects.get(user=u).org.active,
                                   login_url='/checkout/'), name='post')
class CheckoutBeta(View):
    template_name = "logged_in/checkout.html"
    form_class = PaymentForm

    def get(self, request):
        profile = UserProfile.objects.get(user=request.user)
        org = profile.org
        product = Product.objects.get(name="Beta test sensor data")
        plan = Plan.objects.get(product=product, name="sensor data")
        dumpster_count = Dumpster.objects.filter(org=org, active=True).count()
        return render(request, self.template_name, {'stripe_pk': settings.STRIPE_PUBLISHABLE_KEY,
                                                    'email': profile.email.email,
                                                    'amount': plan.charge_amount * dumpster_count,
                                                    'frequency': plan.charge_frequency
                                                    }
                      )

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            try:
                profile = UserProfile.objects.get(user=request.user)
                org = profile.org
                product = Product.objects.get(name="Beta test sensor data")
                plan = Plan.objects.get(product=product, name="sensor data")
                dumpster_count = Dumpster.objects.filter(org=org, active=True).count()

                form = form.cleaned_data

                stripe.api_key = settings.STRIPE_SECRET_KEY
                response = stripe.Customer.create(
                    source=form['stripeToken'],
                    email=profile.email.email,
                )

                data = response['sources']['data'][0]
                payment_method = PaymentMethod.objects.create(last_four_digits=data['last4'],
                                                              card_id=data['id'],
                                                              customer_id=response.id,
                                                              card_type=data['brand'],
                                                              expires=datetime.date(day=1,
                                                                                    month=data['exp_month'],
                                                                                    year=data['exp_year']),
                                                              profile=profile
                                                              )
                start_date = timezone.now()
                if start_date.day > 25:
                    start_date = start_date + relativedelta(months=1)
                start_date = start_date.replace(day=25, hour=0, minute=0, second=0, microsecond=0)
                subscription = stripe.Subscription.create(
                    customer=payment_method.customer_id,
                    items=[{'plan': plan.id,
                            'quantity': dumpster_count
                            }],
                    billing_cycle_anchor=int(time.mktime(start_date.timetuple()))
                )

                sub = Subscription.objects.create(org=org, plan=plan,
                                                  id=subscription.id,
                                                  payment_method=payment_method,
                                                  sensor_count=dumpster_count
                                                  )
                org.active = True
                org.save()
            except Exception as e:
                return render(request, "logged_in/checkout.html", {'stripe_pk': settings.STRIPE_PUBLISHABLE_KEY,
                                                                   'email': profile.email,
                                                                   'amount': plan.charge_amount * dumpster_count,
                                                                   'frequency': plan.charge_frequency,
                                                                   'errors': 'Could not process your payment' + str(e)
                                                                   }
                              )
        else:
            raise ValidationError('Invalid form submission')
        return HttpResponseRedirect(reverse('dashboard'))

