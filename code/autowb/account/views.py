# coding: utf-8
import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import logout as django_logout
from django.core.urlresolvers import reverse

from models import User


def test(request, template):
    user = User(username='testuser')
    user.save()
    testv = datetime.datetime.now()
    return render_to_response(template, {
        'testv': testv,
    }, context_instance=RequestContext(request))


def login(request, template):
    return render_to_response(template, {
    }, context_instance=RequestContext(request))


def logout(request):
    django_logout(request)
    return HttpResponseRedirect(reverse('index'))


def signup_done(request, template, extra_context=None, mimetype=None, **kwargs):
    """
    Render a given template with any extra URL parameters in the context as
    ``{{ params }}``.
    """
    return render_to_response(template, {
    }, context_instance=RequestContext(request))


def user_settings(request, template):
    return render_to_response(template, {
    }, context_instance=RequestContext(request))
