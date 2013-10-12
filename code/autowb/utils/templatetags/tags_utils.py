# coding: utf-8

from django.template import Library
from django.core.files.storage import default_storage
from django.conf import settings

register = Library()


def imgsrc(value):
    if not value:
        return settings.MEDIA_URL + 'img/default.png'

    if value.startswith('http'):
        return value
    else:
        return default_storage.url(value)

register.filter('imgsrc', imgsrc)
