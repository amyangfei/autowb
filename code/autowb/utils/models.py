# coding: utf-8

import uuid
import datetime
from os import path
from PIL import Image
from StringIO import StringIO

from django.core.files.storage import default_storage

from autowb.db import Model


class ImageFileRepo(Model):
    fields = [
        '_id',
        'name',  # full_name
        'size',  # e.g. 140x140
        'meta',
        'original',
        'versions',
        'created',
    ]

    @classmethod
    def create(cls, **kw):
        data = kw.copy()
        data.update({'created': datetime.datetime.now()})
        model = ImageFile(data)
        model.save()
        return model

    @classmethod
    def get_by_name(cls, name):
        return cls.get({'name': name})

    def url(self):
        return default_storage.url(self.name)


def _random_image_name(modifier=None, ext=None):
    modifier = '_' + modifier if modifier else ''
    if not ext:
        ext = 'jpg'

    return '%s%s.%s' % (uuid.uuid4().hex, modifier, ext)


class ImageDataBase:
    def save_with_random_name(self, path, modifier=None):
        ext = self.format if hasattr(self, 'format') else 'jpg'
        image_path = path + _random_image_name(modifier=modifier, ext=ext)
        return self.save(image_path)


class ImageData(ImageDataBase):
    def __init__(self, rawdata):
        self.rawdata = rawdata
        image = Image.open(StringIO(rawdata.read()))
        self.image = image
        self.width, self.height = image.size
        # if original is empty, this file is the original file itself
        self.original = ''
        self.format = image.format

    def save(self, path):
        self.path = default_storage.save(path, self.rawdata)

        model = ImageFileRepo({
            'name': path,
            'size': self.size_str(),
            'meta': '',
            'original': self.original,
            'versions': [],
            'created': datetime.datetime.now()
        })
        model.save()
        return self.path

    def size_str(self):
        return "%sx%s" % (self.width, self.height)

    @classmethod
    def load_from_path(cls, path):
        image = Image.open(path)
        return cls(image)


class ImageFile:
    def __init__(self, fullname):
        self.fullname = fullname
        self.name, self.ext = path.splitext(fullname)

    def name_of_width(self, width, square=False):
        square = 's' if square else ''
        return '%s_w_%s%s%s' % (self.name, square, width, self.ext)
