# coding: utf-8
import hashlib
import random
import datetime
import time

from weibo import APIClient

from autowb.db import Model, get_db
from autowb.utils.images import ImageUtils

db = get_db()


class User(Model):
    fields = [
        '_id',
        'username',
        'password',
        'is_staff',
        'avatar',
        'last_login',
    ]

    @classmethod
    def create_user(cls, *args, **kwargs):
        username = kwargs.get('username', '')
        avatar = kwargs.get('avatar', None)
        password = kwargs.get('password', None)

        user = cls(username=username, avatar=avatar, is_staff=False, last_login=datetime.datetime.now())
        if password:
            user.set_password(password)
        user.save()
        return user

    def set_password(self, raw_pwd):
        algo = 'sha1'
        salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
        pwd_hsh = hashlib.sha1(salt + raw_pwd).hexdigest()
        self.password = '%s$%s$%s' % (algo, salt, pwd_hsh)

    def check_password(self, raw_pwd):
        if not self.password:
            return False
        algo, salt, hsh = self.password.split('$')
        return hsh == hashlib.sha1(salt + raw_pwd).hexdigest()

    def is_authenticated(self):
        return True

    @classmethod
    def get_social_auth(cls, provider, uid):
        if not isinstance(uid, basestring):
            uid = str(uid)
        try:
            return db.UserSocialAuth.find({'provider': provider, 'uid': uid})
        except:
            return None

    def get_social_user(self, provider='weibo'):
        from social_models import UserSocialAuth
        social_users = UserSocialAuth.find({'user_id': self.id, 'provider': provider})
        if social_users.count():
            return social_users[0]
        return None

    def _get_access_token(self, provider="weibo"):
        social_user = self.get_social_user(provider)
        if not social_user:
            return None
        token = social_user.extra_data.get("access_token", "")
        expires_date = social_user.extra_data.get("expires_in", datetime.datetime.now())
        expires = time.mktime(expires_date.timetuple())
        return token, expires

    def get_api(self, provider="weibo"):
        social_user = self.get_social_user(provider)
        if not social_user:
            return None
        api = None
        if provider == 'weibo':
            api = APIClient(app_key="", app_secret="")
        token, expires = self._get_access_token(provider)
        api.set_access_token(access_token=token, expires=expires)
        return api

    def update_weibo(self, wb_cnt):
        client = self.get_api()
        if not client:
            return None
        ret = None
        try:
            if wb_cnt.image_uri:
                img_type, img_data = ImageUtils.get_image_data(wb_cnt.image_uri)
                if img_type == 'http':
                    ret = client.statuses.upload_url_text.post(status=wb_cnt.text, url=img_data)
                elif img_type == 'local':
                    ret = client.statuses.upload.post(status=wb_cnt.text, pic=img_data)
                    img_data.close()
            else:
                ret = client.statuses.update.post(status=wb_cnt.text)
            wb_cnt.do_sent()
        except Exception, e:
            ret = e
        return ret

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return self.id != other.id
