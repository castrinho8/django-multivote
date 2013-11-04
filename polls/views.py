# -*- coding: utf-8 -*-
# Create your views here.

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import generic

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages

from polls.models import Choice, Poll, Vote


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_poll_list'

    def get_queryset(self):
        """Return the last five published polls."""
        return Poll.objects.order_by('-pub_date')[:5]

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        #if not request.user.is_authenticated():
        #    return HttpResponseRedirect(reverse('accounts_login'))
        return super(IndexView, self).get(request, *args, **kwargs)


class DetailView(generic.DetailView):
    model = Poll
    template_name = 'polls/detail.html'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        # print self.__dict__
        context['user_votes'] = Vote.objects.filter(user_id=self.request.user.id)

        print list(context['user_votes'])
        return context

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse('accounts_login'))
        return super(DetailView, self).get(request, *args, **kwargs)


class ResultsView(generic.DetailView):
    model = Poll
    template_name = 'polls/results.html'

    @method_decorator(permission_required('polls.poll_results'))
    def dispatch(self, request, *args, **kwargs):
        return super(ResultsView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse('accounts_login'))

        return super(ResultsView, self).get(request, *args, **kwargs)


@permission_required("polls.bulk")
def bulk_upload(request, poll_id, *args, **kwargs):
    # Delete them all first
    Choice.objects.all().delete()

    created_len = 0
    data = request.POST['data']
    sep = request.POST['sep'] or "\n"

    data_rows = data.split(sep)

    for datum in data_rows:
        datum = datum.strip()
        if not datum:
            continue
        choice, created = Choice.objects.get_or_create(choice_text=datum, poll_id=poll_id, defaults={"suggested_by": request.user})
        if created:
            created_len += 1;

    return HttpResponse("Created %d records." % created_len)


def validate_vote(request_fields, allowed_range, request=None):
    item_values = []
    for key, value in filter(lambda (k, v): 'choice_' in k, request_fields.iteritems()):
        value = int(value)
        key = key[len('choice_'):]
        if value in item_values or value not in allowed_range:
            if request:
                choice = Choice.objects.get(pk=key).choice_text
                messages.debug(request, u"Key = %s (%s), Value = %s, item_values = {%s}, allowed_range = %s" % (key, choice, value, item_values, allowed_range))
            return False
        item_values.append(value)
    return True


@login_required
def vote(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)

    # First of all, delete all votes for this user
    Vote.objects.filter(user=request.user).delete()

    # Filter empty votes
    votes = {}
    for key, value in request.POST.iteritems():
        if value == "0":
            print "Request for key ", key, " not appended"
            continue
        votes[key] = value

    # Validate votes
    if not validate_vote(votes, range(0, 11), request):
        messages.warning(request, u"A votación non pasa a validación interna. Qué carallo andas a facer?")

    else:
        for key, value in filter(lambda (k, v): 'choice_' in k, votes.iteritems()):
            key = key[len('choice_'):]
            cur_choice = Choice.objects.get(pk=key)

            cur_vote, created = Vote.objects.get_or_create(
                number=value, user=request.user,
                defaults={"choice": cur_choice}
            )

            cur_vote.choice = cur_choice
            cur_vote.save()
        messages.success(request, u"Votos rexistrados con éxito.")

    return HttpResponseRedirect(reverse('polls:detail', args=(poll_id,)))

def add_choice(request, poll_id):
    pass
