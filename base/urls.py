from base.views import *
from base.views import CompanycodeView as ccView
from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views

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
    
    #Create an account form
    url(r'^signup/$', AccountView.as_view(), name='signup'),
    url(r'^accounts/success/', SuccessView.as_view(), name='success'),
    url(r'^accounts/accountSuccess/', AccountSuccessView.as_view(), name='accountSuccess'),
    url(r'^companyCode/', ccView.as_view(), name='companyCode'),
    url(r'^accounts/loginSuccess/', LoginSuccessView.as_view(), name='loginSuccess'),
    # Sale cards
    url(r'^tierOne/$', TierOneView.as_view(), name="tierOne"),
    url(r'^tierTwo/$', TierTwoView.as_view(), name="tierTwo"),
    url(r'^tierThree/$', TierThreeView.as_view(), name="tierThree"),
    
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [url(r'^__debug__/', include(debug_toolbar.urls))]
