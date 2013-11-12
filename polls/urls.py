from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import TemplateView

from polls import views

# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^(?P<pk>\d+)/results/$', views.ResultsView.as_view(), name='results'),
    url(r'^(?P<poll_id>\d+)/vote$', views.vote, name='vote'),

    url(r'^(?P<poll_id>\d+)/add_choice$', views.add_choice, name='add_choice'),


    url(r'^(?P<poll_id>\d+)/bulk$', permission_required("polls.bulk")(TemplateView.as_view(template_name="polls/bulk_form.html")), name='bulk'),
    url(r'^(?P<poll_id>\d+)/bulk/upload$', views.bulk_upload, name='bulk_upload'),

)
