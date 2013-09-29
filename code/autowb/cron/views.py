# coding: utf-8

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from autowb.utils.models import WeiboContent


@login_required
def send_test(request, template):
    from time import time
    t_str = str(time())
    wb_cnt = WeiboContent.create(text='test weibo from autowb '+t_str)
    ret = request.user.update_weibo(wb_cnt)
    return render_to_response(template, {
        'ret': ret
    }, context_instance=RequestContext(request))


@login_required
def cron_add(request, template):
    if request.method == 'POST':
        form = EventCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(request.user)
            request.session['ga_event_created_'] = True
            return HttpResponseRedirect(reverse('events'))
    else:
        now = datetime.datetime.now()
        form = EventCreationForm(initial={
            'start_time': now,
            'end_time': now+datetime.timedelta(days=30)
        })
    return render_to_response(template, {
        'form': form
    }, context_instance=RequestContext(request))