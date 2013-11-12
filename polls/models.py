from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Count
from django.utils import timezone


class Poll(models.Model):
    question = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', default=timezone.now)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.question

    def get_votes(self):
        return Vote.objects.all_sorted(self)

    class Meta:
        permissions = (
            ('poll_view', 'Can view polls'),
            ('poll_create', 'Can create a poll'),
            ('poll_vote', 'Can vote in polls'),
            ('poll_results', 'Can view the results of a poll'),
            ('poll_details', 'Can view all the details of a poll'),
            ('bulk', 'Can update choices in bulk'),
            ('full_results', 'Can view the points of each individual choice')
        )

class ChoiceManager(models.Manager):
    def all(self, *args, **kwargs):
        return super(ChoiceManager, self).all(*args, **kwargs).order_by('choice_text')


class Choice(models.Model):
    poll = models.ForeignKey(Poll)
    suggested_by = models.ForeignKey(get_user_model())

    choice_text = models.CharField(max_length=200, unique=True)
    post_date = models.DateTimeField('date posted', default=timezone.now)

    objects = ChoiceManager()

    def __unicode__(self):
        return self.choice_text


class VoteManager(models.Manager):
    def all_sorted(self, poll):

        choices = Choice.objects.filter(poll=poll)
        qs = self.filter(choice__in=choices)
        # qs = qs.order_by('number__sum')
        # qs = qs.extra(select={ 'nsum' : 'SUM(number)' }, order_by='-nsum')
        qs = qs.select_related('choice').values('choice__choice_text').annotate(models.Sum('number'), models.Count('number')).order_by('-number__count', '-number__sum')

        print qs
        print "hola!"
        return qs

    def get_users(self):
        x = self.values("user").annotate(Count("id")).order_by()

        print x
        return x



class Vote(models.Model):
    choice = models.ForeignKey(Choice)
    user = models.ForeignKey(get_user_model())

    number = models.IntegerField()
    post_date = models.DateTimeField('date posted', default=timezone.now)

    objects = VoteManager()

    def __unicode__(self):
        return u"{0}p: {1} -> {2}".format(self.number, self.user, self.choice)


