from trashr.views import *
from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views, logout

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    # Landing pages
    url(r'^$', IndexView.as_view(), name="index"),
    url(r'^services/$', ServicesView.as_view(), name="services"),
    url(r'^technology/$', TechnologyView.as_view(), name="technology"),
    url(r'^about/$', AboutView.as_view(), name="about"),
    url(r'^privacy/$', PrivacyView.as_view(), name='privacy'),
    url(r'^TaC/$', TermsView.as_view(), name='terms'),
    url(r'^contact/$', ContactView.as_view(), name='contact'),

    # REST APIs
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^create/', CreateReading.as_view(), name="create"),
    url(r'^create-trans/', CreateTransaction.as_view(), name="create-trans"),

    # Login actions
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^signup/$', AccountView.as_view(), name='signup'),
    url(r'^logout/$', logout, {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),

    # Logged in pages
    url(r'^dashboard/$', DashboardView.as_view(), name='dashboard'),
    url(r'^graph/', GraphView.as_view(), name='graph'),
    url(r'^preferences/', PreferencesView.as_view(), name='preferences'),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^alert_update/', AlertUpdateView.as_view(), name='alert_update'),

    # Account actions
    url(r'^accounts/success/', SuccessView.as_view(), name='success'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/(?P<email>[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)/$',
        ActivateAccount.as_view(), name='activate'),
    url(r'^reset_confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        ResetConfirm.as_view(), name='password_reset_confirm'),

    # Email confirmations
    url(r'^email-autocomplete/$', EmailAutoComplete.as_view(), name='email-autocomplete'),
    url(r'^email-delete/$', EmailDelete.as_view(), name='email-delete'),
    url(r'^email-verify/$', EmailVerify.as_view(), name='email-verify'),

    # Payment pages
    url(r'^checkout/$', CheckoutBeta.as_view(), name="checkout"),
    url(r'^payment-update/$', PaymentUpdate.as_view(), name="payment_update"),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [url(r'^__debug__/', include(debug_toolbar.urls))]
