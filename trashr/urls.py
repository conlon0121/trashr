from trashr.views import *
from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views, logout

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^$', IndexView.as_view(), name="index"),
    url(r'^create/', CreateReading.as_view(), name="create"),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^dashboard/$', DashboardView.as_view(), name='dashboard'),
    url(r'^demo/$', DemoView.as_view(), name='demo'),
    url(r'^graph/', GraphView.as_view(), name='graph'),
    url(r'^preferences/', PreferencesView.as_view(), name='preferences'),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^alert_update/', AlertUpdateView.as_view(), name='alert_update'),

    url(r'^signup/$', AccountView.as_view(), name='signup'),
    url(r'^logout/$', logout, {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
    url(r'^accounts/success/', SuccessView.as_view(), name='success'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/(?P<email>[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)/$',
        ActivateAccount.as_view(), name='activate'),
    url(r'^reset_confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        ResetConfirm.as_view(), name='password_reset_confirm'),
    url(r'^email-autocomplete/$', EmailAutoComplete.as_view(), name='email-autocomplete'),
    url(r'^email-delete/$', EmailDelete.as_view(), name='email-delete'),
    url(r'^email-verify/$', EmailVerify.as_view(), name='email-verify'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [url(r'^__debug__/', include(debug_toolbar.urls))]
