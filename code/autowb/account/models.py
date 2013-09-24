# coding: utf-8
import hashlib
import random
import datetime

from autowb.db import Model, get_db

db = get_db()


class User(Model):
    fields = [
        '_id',
        # 'pk',
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

    def _update(self, doc):
        self.get_collection().update({'_id': self.id}, {'$set': doc})

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return self.id != other.id
