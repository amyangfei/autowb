# coding: utf-8
import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from models import User
from forms import PriorityTokenForm


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


@login_required
def user_settings(request, template):
    return render_to_response(template, {
    }, context_instance=RequestContext(request))


def edit_pri_access_token(request, template):
    if request.method == 'POST':
        form = PriorityTokenForm(request.user, data=request.POST)
        if form.is_valid():
            form.save(request.user)
            return HttpResponseRedirect(reverse('edit_pri_access_token'))
    else:
        form = PriorityTokenForm(request.user)
    return render_to_response(template, {
        'form': form,
    }, context_instance=RequestContext(request))
