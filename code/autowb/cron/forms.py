# coding: utf-8
import datetime

from django import forms
from django.forms.extras.widgets import SelectDateWidget

from autowb.cron.models import WeiboContent
from autowb.utils.images import ImageUtils
from autowb.scheduler import get_scheduler


HOUR_CHOICES = [(x, x) for x in range(24)]
MINUTE_CHOICES = [(x, x) for x in range(60)]
_MIN_TIME_DELTA = 1


def _send_weibo(user, wb_cnt):
    user.update_weibo(wb_cnt)


def _add_scehduler(callback, user, wb_cnt):
    scheduler = get_scheduler()
    scheduler.add_date_job(callback, date=wb_cnt.push_date, args=[user, wb_cnt, ])
    # scheduler.add_cron_job(callback, hour='0-23', minute='0-59', second='30', args=['world'])


class CronForm(forms.Form):
    text = forms.CharField(
        label=u'weibo text',
        widget=forms.Textarea(),
        required=False,
    )
    send_date = forms.DateTimeField(label=u'发送时间', widget=SelectDateWidget(years=range(datetime.datetime.now().year, datetime.datetime.now().year + 2)))
    hour = forms.ChoiceField(label='时', widget=forms.Select(), choices=HOUR_CHOICES)
    minute = forms.ChoiceField(label='分', widget=forms.Select(), choices=MINUTE_CHOICES)

    image = forms.ImageField(
        label=u'图片',
        widget=forms.ClearableFileInput(attrs={'class': 'input-h'}),
        required=False,
    )

    def clean(self):
        cd = super(CronForm, self).clean()
        errors = []
        if not cd.get('text'):
            errors.append(u'您必须说点什么')
        # preview_uri = cleaned_data.get('preview')
        # if not preview_uri or not ImageUtils.is_image_exists(preview_uri):
        #     errors.append(u'您必须上传图片')
        _date = cd.get('send_date', datetime.datetime.now())
        _hour = int(cd.get('hour', '0'))
        _minute = int(cd.get('minute', '0'))
        if datetime.datetime(_date.year, _date.month, _date.day, _hour, _minute) < datetime.datetime.now() + datetime.timedelta(minutes=_MIN_TIME_DELTA):
            errors.append(u'错误的发送时间')
        if errors:
            raise forms.ValidationError(errors)
        return cd

    def save(self, user):
        cd = self.cleaned_data
        _date = cd.get('send_date', datetime.datetime.now())
        _hour = int(cd.get('hour', '0'))
        _minute = int(cd.get('minute', '0'))

        image_uri = ImageUtils.handle_weibo_image(cd['image']) if cd['image'] else None

        wb_cnt = WeiboContent.create(
            user_id=user.id,
            username=user.username,
            text=cd['text'],
            push_date=datetime.datetime(_date.year, _date.month, _date.day, _hour, _minute),
            image_uri=image_uri,
        )
        _add_scehduler(_send_weibo, user, wb_cnt)
        return wb_cnt
