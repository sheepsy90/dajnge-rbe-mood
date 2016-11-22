from django.conf import settings

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.template import RequestContext

from rbe_authorize.api.api import get_user_identity


def landing(request):
    if hasattr(request, 'user') and request.user.is_authenticated:
        return HttpResponseRedirect(settings.AFTER_LOGIN_URL)
    return render(request, 'polls/landing.html')


@login_required(login_url=settings.LOGIN_URL)
def index(request):
    return render(request, 'polls/index.html')


def error_page(request):
    rc = RequestContext(request)
    return render_to_response('polls/error_page.html', rc)


@login_required(login_url=settings.LOGIN_URL)
def refresh_profile(request):
    access_token = request.user.profile.token.access_token
    print access_token
    result = get_user_identity(access_token)
    return render(request, 'polls/index.html', {'token_stuff': result})
