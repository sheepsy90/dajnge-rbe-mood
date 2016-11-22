from django.conf import settings

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.template.context import RequestContext

from rbe_authorize.api.api import get_user_identity


def landing(request):
    if hasattr(request, 'user') and request.user.is_authenticated:
        return HttpResponseRedirect(settings.AFTER_LOGIN_URL)
    return render(request, 'polls/landing.html')


@login_required(login_url=settings.LOGIN_URL)
def index(request):
    return render(request, 'polls/index.html')


@login_required(login_url=settings.LOGIN_URL)
def settings_page(request):
    return render(request, 'polls/settings_page.html')


def error_page(request):
    rc = RequestContext(request)
    return render_to_response('polls/error_page.html', rc)


@login_required(login_url=settings.LOGIN_URL)
def question_types(request):
    return render(request, 'polls/question_types.html')
