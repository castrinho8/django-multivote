from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse

from cas_client import views

urlpatterns = patterns('',
    url(r'^$', views.cas_redirect, name='cas-redirect'),
    url(r'^cas$', views.login_view, name='cas-callback'),
    url(r'^logout$', views.logout_view, name='cas-logout'),

)
