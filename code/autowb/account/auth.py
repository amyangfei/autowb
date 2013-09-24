# coding: utf-8
import datetime
from django.contrib.auth.signals import user_logged_in
from models import User
# from forms import unify_email


class UserBackend(object):
    supports_object_permissions = False
    supports_anonymous_user = True

    def authenticate(self, username=None, password=None):
        user = User.get({'username': username})
        return user

    def get_user(self, user_id):
        user = User.get_by_id(user_id)
        return user

# def update_last_login(sender, user, **kwargs):
#     """
#     A signal receiver which updates the last_login date for
#     the user logging in.
#     """
#     user.last_login = datetime.datetime.now()
#     user.save()
# user_logged_in.connect(update_last_login)

