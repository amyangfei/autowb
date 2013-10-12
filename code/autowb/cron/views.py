# coding: utf-8

import datetime

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from autowb.cron.models import WeiboContent
from autowb.cron.forms import CronForm, TestForm
from autowb.scheduler import get_scheduler


@login_required
def send_test(request, template):
    ret = None
    if request.method == 'POST':
        form = TestForm(request.POST, request.FILES)
        if form.is_valid():
            ret = form.save(request.user)
    else:
        form = TestForm()
    return render_to_response(template, {
        'form': form,
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


@login_required
def cron_delete(request, wbcnt_id):
    wb_cnt = WeiboContent.get_by_id(wbcnt_id)
    if not wb_cnt or wb_cnt.user_id != request.user.id:
        messages.success(request, u'错误的操作!')
        return HttpResponseRedirect(reverse('cron_unsent_list'))
    if request.method == 'POST':
        # FIXME: not good, get all jobs and iterate them
        scheduler = get_scheduler()
        jobs = scheduler.get_jobs()
        for job in jobs:
            if job.name == wbcnt_id:
                scheduler.unschedule_job(job)
        wb_cnt.delete()
    return HttpResponseRedirect(reverse('cron_unsent_list'))


@login_required
def cron_unsent_list(request, template):
    unsent = WeiboContent.find({'user_id': request.user.id, 'sent': False}, sort=[('push_date', 1)])
    return render_to_response(template, {
        'unsent': unsent,
    }, context_instance=RequestContext(request))


@login_required
def cron_s_unsent_list(request, template):
    scheduler = get_scheduler()
    scheduler_unsent = scheduler.get_jobs()
    return render_to_response(template, {
        'scheduler_unsent': scheduler_unsent,
    }, context_instance=RequestContext(request))
