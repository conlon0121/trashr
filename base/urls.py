from base.views import *
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.views.generic.base import RedirectView
from rest_framework import routers, serializers, viewsets

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
    url(r'^dumpster_filter_table/', DumpsterFilterTable.as_view(), name='filter_table')
]
