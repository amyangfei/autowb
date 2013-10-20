# coding: utf-8
import datetime

from django import forms

from weibo import APIClient


def _get_priority_data(access_token):
    if not access_token:
        return {'access_token': None, 'expires_in': None, 'uid': None}
    client = APIClient('', '')
    client.access_token = access_token
    try:
        res = client.get_token_info(access_token)
        expire_time = res.get('expire_in', '') + res.get('create_at', '')
        expires_in = datetime.datetime.fromtimestamp(expire_time)
        uid = res.get('uid')
    except:
        return None
    return {'access_token': access_token, 'expires_in': expires_in, 'uid': uid}


class PriorityTokenForm(forms.Form):
    priority_access_token = forms.CharField(
        label=u'priority access token',
        widget=forms.TextInput(attrs={'size': '50'}),
        required=False,
    )

    expires_in = forms.CharField(
        label=u'access_token过期时间',
        widget=forms.TextInput(attrs={'size': '30'}),
        required=False,
    )

    def __init__(self, user, *a, **kw):
        priority_data = user.get_priority_data()
        super(PriorityTokenForm, self).__init__(initial={
            'priority_access_token': priority_data.get('access_token'),
            'expires_in': priority_data.get('expires_in')}, *a, **kw)
        self.priority_data = {}

    def clean(self):
        cd = super(PriorityTokenForm, self).clean()
        errors = []
        # validation of access_token
        priority_data = _get_priority_data(cd.get('priority_access_token'))
        self.priority_data = priority_data
        if not priority_data:
            errors.append(u'错误的或过期的access_token')
        if errors:
            raise forms.ValidationError(errors)
        return cd

    def save(self, user):
        priority_data = self.priority_data
        user.update_priority_data(**priority_data)
