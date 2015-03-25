from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.utils.functional import SimpleLazyObject

from settings import FAMILY_HOST
def get_user(request):
    if not hasattr(request, '_cached_user'):
        request._cached_user = auth.get_user(request)
    return request._cached_user

class LoginMiddleware(object):
    def process_request(self, request):
        assert hasattr(request, 'session'), "The Django authentication middleware requires session middleware to be installed. Edit your MIDDLEWARE_CLASSES setting to insert 'django.contrib.sessions.middleware.SessionMiddleware'."
        request.user = SimpleLazyObject(lambda: get_user(request))
        if request not in []:
            login_required(login_url = FAMILY_HOST+'/user/login')