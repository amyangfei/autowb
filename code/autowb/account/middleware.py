# -*- coding: UTF-8 -*-
from django.core.urlresolvers import reverse

from social_auth.exceptions import AuthAlreadyAssociated
from social_auth.middleware import SocialAuthExceptionMiddleware


class AutowbSocialAuthExceptionMiddleware(SocialAuthExceptionMiddleware):
    def get_message(self, request, exception):
        if isinstance(exception, AuthAlreadyAssociated):
            return u"该账号已经被某人绑定过了"
        return u"正在施工中"

    def get_redirect_uri(self, request, exception):
        return reverse('user_settings')
