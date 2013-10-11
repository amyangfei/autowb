# coding: utf-8

import datetime

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from autowb.cron.models import WeiboContent
from autowb.cron.forms import CronForm


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
        form = CronForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(request.user)
            messages.success(request, u'添加推送微博任务成功')
            return HttpResponseRedirect(reverse('cron_add'))
    else:
        s_date = datetime.datetime.now() + datetime.timedelta(minutes=5)
        form = CronForm(initial={'send_date': s_date, 'hour': s_date.hour, 'minute': s_date.minute})

    recent_cron = WeiboContent.find({'user_id': request.user.id}, sort=[('created', -1)], limit=1)

    return render_to_response(template, {
        'form': form,
        'recent_cron': recent_cron,
    }, context_instance=RequestContext(request))
