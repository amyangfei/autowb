# coding: utf-8

import datetime

from apscheduler.scheduler import Scheduler

from autowb.account.models import User
from autowb.cron.models import WeiboContent


def default_callback(user, wb_cnt):
    return user.update_weibo(wb_cnt)

wb_cnt_unsent = WeiboContent.find({'sent': False, 'push_date': {'$gt': datetime.datetime.now()}})

# _scheduler = Scheduler(daemonic=False)
_scheduler = Scheduler()

# reload unsent job
for wb_cnt in wb_cnt_unsent:
    user = User.get_by_id(wb_cnt.user_id)
    _scheduler.add_date_job(default_callback, date=wb_cnt.push_date, name=str(wb_cnt.id), args=[user, wb_cnt, ])

_scheduler.start()


def get_scheduler():
    return _scheduler
