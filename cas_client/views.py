from django.conf import settings
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.views.decorators.http import require_GET, require_safe
from django.contrib.auth import authenticate, login, logout, get_user_model, get_backends
from django.contrib.auth.decorators import user_passes_test

from cas_client.models import get_service_url


@require_safe
def cas_redirect(request):
    # Save 'next' parameter if set
    if 'next' in request.REQUEST:
        request.session['login_redirect'] = request.REQUEST['next']

    url = settings.CAS_URL % ('login?service=%s')
    service = get_service_url(request, True)

    redirect_url = url % (service)

    return HttpResponseRedirect(redirect_url)

@require_GET
def login_view(request):
    ticket = request.GET['ticket']
    service = get_service_url(request)

    user = authenticate(service=service, ticket=ticket)
    if user is not None:
        # ticket was correct
        login(request, user)


    redirect_url = "/"
    if 'login_redirect' in request.session:
        redirect_url = request.session['login_redirect']
        del request.session['login_redirect']

    return HttpResponseRedirect(redirect_url)
    return HttpResponse('User is authenticated? ' + str(request.user.is_authenticated()))


def logout_view(request):
    logout(request)

    return HttpResponseRedirect('/')
