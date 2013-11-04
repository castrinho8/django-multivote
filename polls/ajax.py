# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from dajax.core import Dajax
from polls.models import Choice, Poll
from dajaxice.decorators import dajaxice_register


@dajaxice_register
def add_choice(request, **kwargs):
    dajax = Dajax()

    if not request.user.is_authenticated():
        dajax.add_data(request.user.id, 'console.log')
        return dajax.json()

    poll_id = kwargs['poll_id']
    choice_text = kwargs['text']

    p = Poll.objects.get(pk=poll_id)

    # Check whether it already exists...
    choice = Choice.objects.filter(choice_text__icontains=choice_text)
    if choice:
        print "Already exists!"
        print "Not appending."
        dajax.add_data('Choice ' + choice[0].choice_text + ' already exists', 'console.log')
        dajax.add_data('A posibilidade ' + choice[0].choice_text + ' xa existe.', 'add_ajax_error')
        return dajax.json()

    choice = Choice(poll=p, suggested_by=request.user, choice_text=choice_text)
    choice.save()

    html = u'''<li><label style="display:inline">
    <input type="text" class="score_input input-mini"
    name="choice_{ID}" placeholder="1..10" id="choice_{ID}"
    value="0" style="margin-right: 1em"/>
        {TEXT}
    </label></li>'''

    html = html.format(ID=choice.id, TEXT=choice.choice_text)

    dajax.append('#sortable', 'innerHTML', html)
    dajax.add_data(choice.id, 'attach_on_change')
    return dajax.json()

@dajaxice_register
def edit_choice_name(request, **kwargs):
    dajax = Dajax()

    if not request.is_authenticated():
        dajax.add_data(request.user.id, 'console.log')
        return dajax.json()

    poll_id = kwargs['poll_id']
    choice_id = kwargs['id']
    choice_text = kwargs['text']

    choice = Choice.objects.get(pk=choice_id)

    # Check if there are any votes with it.
    # If there are any, prohibit request
    votes = Vote.objects.filter(choice=choice)

    if len(votes) > 0:
        # Request is forbidden
        dajax.add_data("Xa non se pode modificar esta opción.", "visual_warn")
        return dajax.json()

    # Check whether the user did create the thing
    if choice.suggested_by != request.user:
        print "User %s did not suggest choice %s (%s)" % (request.user, choice, choice.suggested_by)
        dajax.add_data("Xa non se pode modificar esta opción.", "visual_warn")
        return dajax.json()

    # Now everything should be checked out
    # Change the text and update
    choice.choice_text = choice_text
    choice.save()

    dajax.add_data(choice_text, "function(txt){choices[" + choice_id + "] = txt; drawswap_choice(choice_id, txt)}")
