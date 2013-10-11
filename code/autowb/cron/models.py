# coding: utf-8

import datetime

from autowb.db import Model
from autowb.account.models import User


class WeiboContent(Model):
    fields = [
        '_id',
        'push_date',
        'created',
        'text',
        'image_uri',
        'user_id',
        'username',
        'sent',
        'sent_time',
    ]

    @classmethod
    def create(cls, **kw):
        data = kw.copy()
        now = datetime.datetime.now()
        data.update({'created': now, 'sent': False})
        wb_cnt = WeiboContent(data)
        wb_cnt.save()
        return wb_cnt

    def get_user(self):
        return User.get_by_id(self.user_id)

    def do_sent(self):
        self.sent = True
        self.sent_time = datetime.datetime.now()
        self.save()
