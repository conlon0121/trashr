from base.views import *
from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    #url(r'^$', IndexView.as_view(), name="index"),
    url(r'^$', IndexView.as_view(), name="index"),
    url(r'^create/', CreateReading.as_view(), name="create"),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^dashboard/$', DashboardView.as_view(), name='dashboard'),
    url(r'^demo/$', DemoView.as_view(), name='demo'),
    url(r'^graph/', GraphView.as_view(), name='graph'),
    url(r'^route/', RouteView.as_view(), name='route'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [url(r'^__debug__/', include(debug_toolbar.urls))]
