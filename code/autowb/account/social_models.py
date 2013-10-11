# coding: utf-8

import base64

from pymongo.objectid import ObjectId

from autowb.db import Model
from social_auth.db.base import UserSocialAuthMixin, AssociationMixin

from models import User


#for social auth
class UserSocialAuth(Model, UserSocialAuthMixin):
    """Social Auth association model"""
    User = User
    fields = [
        '_id',
        'user_id',
        'provider',
        'uid',  # each model should have an uri method to get direct to resource view
        'extra_data',
        'priority_data',  # high priority, special useage
    ]

    def _set_user(self, user):
        setattr(self, 'user_id', user.id)

    def _get_user(self):
        return self.User.get_by_id(self.user_id)
    user = property(_get_user, _set_user)

    def basic_attrs(self):
        keys = ['provider', 'uid', 'extra_data']
        return [(k, self.__dict__[k]) for k in keys]

    @classmethod
    def get_social_auth_for_user(cls, user):
        #hacker for django_social_auth
        def _filter(self, provider):
            for o in self:
                if o.provider == provider:
                    return o

        #return [o for o in self if o.provider == provider]
        def _get(self, id):
            for o in self:
                if o.id == ObjectId(id):
                    return o
        import new
        from db import Model
        social_users = UserSocialAuth.find({'user_id': user.id})
        social_users.filter = new.instancemethod(_filter, social_users, Model)
        social_users.get = new.instancemethod(_get, social_users, social_users.__class__)
        return social_users

    @classmethod
    def username_max_length(cls):
        #return User.username.max_length
        return 255

    @classmethod
    def simple_user_exists(cls, *args, **kwargs):
        """
        Return True/False if a User instance exists with the given arguments.
        Arguments are directly passed to filter() manager method.
        """
        #TODO ...
        #return User.find(*args, **kwargs).count() > 0
        return cls.User.find(kwargs).count() > 0

    @classmethod
    def create_user(cls, *args, **kwargs):
        print 'UserSocialAuth create_user', kwargs
        return cls.User.create_user(*args, **kwargs)

    @classmethod
    def get_user(cls, pk):
        try:
            return cls.User.get_by_id(pk)
        except:
            return None

    @classmethod
    def get_user_by_email(cls, email):
        return cls.User.get({'email': email})

    @classmethod
    def resolve_user_or_id(cls, user_or_id):
        if isinstance(user_or_id, User):
            return user_or_id
        return cls.User.get({'pk': user_or_id})

    @classmethod
    def get_social_auth(cls, provider, uid):
        if not isinstance(uid, basestring):
            uid = str(uid)
        try:
            return UserSocialAuth.get({'provider': provider, 'uid': uid})
        except:
            return None

    @classmethod
    def create_social_auth(cls, user, uid, provider):
        if not isinstance(uid, basestring):
            uid = str(uid)
        social_auth = UserSocialAuth(user_id=user.id, uid=uid, provider=provider)
        social_auth.save()
        return social_auth

    @classmethod
    def store_association(cls, server_url, association):
        #from social_auth.models import Association
        args = {'server_url': server_url, 'handle': association.handle}
        try:
            assoc = Association.get(**args)
        except:
            assoc = Association(**args)
        assoc.secret = base64.encodestring(association.secret)
        assoc.issued = association.issued
        assoc.lifetime = association.lifetime
        assoc.assoc_type = association.assoc_type
        assoc.save()

    @classmethod
    def delete_associations(cls, ids_to_delete):
        #from social_auth.models import Association
        #TODO to check
        for id in ids_to_delete:
            Association.get_by_id(id).delete()
        #Association.find(pk__in=ids_to_delete).delete()

    @classmethod
    def allowed_to_disconnect(cls, user, backend_name, association_id=None):
        return True


class Association(Model, AssociationMixin):
    """OpenId account association"""
    fields = [
        '_id',
        'handle',
        'secret',
        'issued',
        'lifetime',
        'assoc_type',
    ]


def is_integrity_error(exc):
    return exc.__class__ is AttributeError
