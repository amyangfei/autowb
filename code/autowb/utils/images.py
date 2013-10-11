# coding: utf-8

from django.core.files.storage import default_storage

from autowb.utils.models import ImageData


class ImageUtils(object):

    WEIBO_IMAGE = 'uploads/weibo/'

    MODIFIER_RESIZED = 'resized'

    @staticmethod
    def _save_raw(rawdata, path, modifier=None):
        image = ImageData(rawdata)
        return image.save_with_random_name(path, modifier)

    @staticmethod
    def handle_weibo_image(rawdata):
        return ImageUtils._save_raw(rawdata, ImageUtils.WEIBO_IMAGE)

    @staticmethod
    def get_image_data(image_uri):
        if image_uri.startswith('http'):
            return 'http', image_uri
        return 'local', default_storage.open(image_uri)

    @classmethod
    def is_image_exists(image_uri):
        if image_uri.startswith('http'):
            # to be supported later
            return True
        else:
            return default_storage.exists(default_storage.path(image_uri))

    # @staticmethod
    # def delete(image_uri):
    #     image_file = ImageFile(image_uri)
    #     return image_file.delete()
