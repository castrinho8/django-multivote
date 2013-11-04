from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from dajaxice.core import dajaxice_autodiscover, dajaxice_config
dajaxice_autodiscover()

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView

from django.contrib.auth.views import login

from cas_client import views


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'orlaudc.views.home', name='home'),
    # url(r'^orlaudc/', include('orlaudc.foo.urls')),

    url (r'^$', TemplateView.as_view(template_name="home.html"),
            name='home'),

    url(r'^polls/', include('polls.urls', namespace="polls")),
    url(r'^cas/', include('cas_client.urls')),

    url(r'^accounts/login',
    		TemplateView.as_view(template_name="accounts_login.html"),
    		name='accounts_login'),

    url(r'^accounts/local_login', login, name="login"),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
    
)
urlpatterns += staticfiles_urlpatterns()
