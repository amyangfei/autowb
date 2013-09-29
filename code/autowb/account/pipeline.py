# -*- coding: UTF-8 -*-

from django.conf import settings


def avatar(backend, details, response, user=None, *args, **kwargs):
    if not user:
        return
    avatar_key = getattr(settings, 'SOCIAL_AUTH_AVATAR_KEY', {}).get(backend.name)
    avatar_uri = response.get(avatar_key, '')
    if not user.avatar:
        user.avatar = avatar_uri
        user.save()
