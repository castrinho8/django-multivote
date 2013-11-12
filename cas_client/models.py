from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, User
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from django.core.urlresolvers import reverse

def get_service_url(request, urlencoded=False):
    '''
    Helper function to get the service parameter to put in the url
    get a nice redirect from the CAS server.
    '''
    service = reverse('cas-callback')

    scheme = request.META['wsgi.url_scheme']
    server = request.META['SERVER_NAME']
    port = ':' + request.META['SERVER_PORT']
    if scheme == 'http' and port == '80':
        port = ''
    if scheme == 'https' and port == '443':
        port = ''

    url = "{0}://{1}{2}{3}".format(scheme, server, port, service)

    if urlencoded:
        import urllib
        return urllib.quote_plus(url)
    else:
        return url


class CasUserManager(BaseUserManager):
    def create_user(self, login, rawdata=None, password=None):
        if not rawdata:
            pass

        user = self.model(
            login=login,
            rawdata=rawdata,
            password=password
        )

        user.save(using=self._db)
        return user

    def create_superuser(self, login, rawdata, password):

        user = self.model(
            login=login,
            rawdata=rawdata,
            is_staff=True,
            is_active=True,
            password=password
        )

        user.save(using=self._db)
        return user


class CasUser(AbstractBaseUser):
    login = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    last_token = models.CharField(max_length=128)
    rawdata = models.TextField()

    # These may be specific to only some CAS providers
    doctype = models.CharField(max_length=12)
    nif = models.CharField(max_length=12)

    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = [ 'rawdata' ]

    objects = CasUserManager()

    class Meta:
        permissions = (
            ('user_view', 'Can view individual users'),
            ('user_role_view', 'View roles of an user'),
        )

    def __unicode__(self):
        return self.login

    def get_full_name(self):
        return "{0} {1}".format(self.first_name, self.last_name)

    def get_short_name(self):
        return self.login

    def has_perm(self, perm, obj=None):
        if not self.is_active:
            return False

        if self.is_staff:
            return True

        if perm in [ #'polls.poll_results',
            'polls.bulk',
            'polls.full_results']:
            return False
        return True

    def has_module_perms(self, app_label):
        return app_label in settings.CAS_ENABLED_APPS


class CasRole(models.Model):
    name = models.CharField(max_length=100)
    users = models.ManyToManyField(CasUser)

    def __unicode__(self):
        return name

    class Meta:
        permissions = (
            ('role_view', 'View roles associated to a user'),
        )


from django.conf import settings

class CasBackend(object):

    def get_user(self, pk):
        return CasUser.objects.get(pk=pk)

    def authenticate(self, service=None, ticket=None):
        # Do the ticket verification

        raw_data = self.perform_remote_validation(service, ticket)
        data = self.parse_cas_xml(raw_data)

        if not data:
            return None

        login = data['login']
        first_name = data['first_name']
        last_name = data['last_name']

        user, created = CasUser.objects.get_or_create(login=login, defaults={
            'first_name':first_name,
            'last_name':last_name,
            'last_token':ticket,
            'rawdata':raw_data})

        user.last_token = ticket
        user.save()

        # Try and append user to each role
        for role_name in data['roles']:
            # Create role if it didn't exist yet
            role, created = CasRole.objects.get_or_create(name=role_name)
            role.users.add(user)

        return user

    def parse_cas_xml(self, raw):
        from lxml import etree
        CAS = '{http://www.yale.edu/tp/cas}'

        try:
            xml = etree.fromstring(raw)
            root = xml.find(CAS + 'authenticationSuccess')
        except etree.XMLSyntaxError:
            print "Error, XML is probably not UTF8 or not XML"
            print raw
            return None

        if root is None:
            # Authentication unsuccessful
            return None

        _attrib = root.find(CAS + 'attributes')
        def attrib (s):
            try:
                return _attrib.find(CAS + s).text
            except:
                return u'-not-found-'

        def get_roles(attrib=attrib):
            rolestring = attrib('roles')

            if rolestring[0] == '[' and rolestring[-1] == ']':
                rolestring = rolestring[1:-1]

            return map(unicode.strip, rolestring.split(','))

        data = {
            'login': root.find(CAS + 'user').text,
            'first_name': attrib('firstName'),
            'last_name': attrib('surname1') + ' ' + attrib('surname2'),
            'doctype': attrib('documentType'),
            'nif': attrib('documentNumber'),
            'roles': get_roles(),
        }

        return data

    def perform_remote_validation(self, service, ticket):
        import urllib2
        import urllib

        params = urllib.urlencode({'service': service, 'ticket': ticket}, True)
        verify_url = settings.CAS_URL % ('serviceValidate?%s' % (params))
        print "Opening request against URL: %s" % verify_url
        request = urllib2.urlopen(verify_url)
        raw_data = request.read()
        request.close()

        return raw_data




