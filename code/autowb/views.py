# coding: utf-8

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from autowb.utils.models import WeiboContent


def index(request, template):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('home'))
    else:
        return HttpResponseRedirect(reverse('login'))


@login_required
def home(request, template):
    return render_to_response(template, {
    }, context_instance=RequestContext(request))


@login_required
def send_test(request, template):
    from time import time
    t_str = str(time())
    wb_cnt = WeiboContent.create(text='test weibo from autowb '+t_str)
    ret = request.user.update_weibo(wb_cnt)
    return render_to_response(template, {
        'ret': ret
    }, context_instance=RequestContext(request))
