# coding: utf-8
import settings
from pymongo import Connection
from pymongo.objectid import ObjectId

_connection = Connection(settings.MONGODB_HOST, settings.MONGODB_PORT)
_db = _connection[settings.MONGODB_NAME]


def get_db():
    return _db


def to_objectid(oid):
    if oid is None or isinstance(oid, ObjectId):
        return oid
    if isinstance(oid, basestring):
        try:
            oid = ObjectId(oid)
        except:
            oid = None
        return oid


class Model(object):
    __colname = None

    def __init__(self, doc=None, **kwargs):
        self._id = None
        if doc is None:
            doc = {}
        doc.update(kwargs)
        for field in self.fields:
            val = doc.get(field, None)
            setattr(self, field, val)
        # setattr(self, 'pk', self._id)

    def _set_id(self, id):
        setattr(self, '_id', id)

    def _get_id(self):
        return self._id
    id = property(_get_id, _set_id)

    def _set_pk(self, pk):
        setattr(self, '_pk', pk)

    def _get_pk(self):
        return self._id
    pk = property(_get_pk, _set_pk)

    @classmethod
    def get(cls, spec):
        doc = cls.get_collection().find_one(spec)
        if doc:
            return cls(doc=doc)
        return None

    @classmethod
    def get_by_id(cls, _id):
        return cls.get({u'_id': to_objectid(_id)})

    @classmethod
    def find(cls, *args, **kwargs):
        return MongoQuerySet(cls.get_collection().find(*args, **kwargs), cls)

    @classmethod
    def get_collection(cls):
        if hasattr(cls, '__colname') and not cls.__colname:
            return _db[cls.__colname.lower()]
        return _db[cls.__name__.lower()]

    @classmethod
    def get_db(cls):
        return _db

    def to_python(self):
        data = {}
        for k in self.fields:
            data[k] = getattr(self, k, None)
        data.pop('_id', None)
        return data

    @classmethod
    def create(cls, **kw):
        obj = cls(**kw)
        obj.save()
        return obj

    def save(self, **kwargs):
        data = self.to_python()
        if self.id:
            self.get_collection().update({'_id': self.id}, {'$set': data})
        else:
            self.id = self.get_collection().insert(data)

    def update(self, data):
        assert self.id
        doc = self.to_python()
        for k, v in data.iteritems():
            if k in doc:
                doc[k] = v
        self.get_collection().update({'_id': self.id}, {'$set': doc})

    def delete(self):
        self.get_collection().remove({'_id': self.id})


class MongoQuerySet(object):
    """Return a MongoQuerySet object used for Django object_list
    """

    def __init__(self, cursor, model_class):
        self._cursor = cursor
        self.model_class = model_class

    def count(self):
        return self._cursor.count(with_limit_and_skip=True)

    def __len__(self):
        return self.count()

    def __getitem__(self, key):
        # Slice provided
        if isinstance(key, slice):
            try:
                return (self.model_class(doc) for doc in self._cursor[key])
            except IndexError, err:
                start = key.start or 0
                if start >= 0 and key.stop >= 0 and key.step is None:
                    if start == key.stop:
                        return []
                raise err
            # slice count limited to small number
            return [self.model_class(doc) for doc in self._cursor[key]]
        elif isinstance(key, int):
            return self.model_class(self._cursor[key])

    def __iter__(self):
        for doc in self._cursor:
            yield self.model_class(doc)

    def _clone(self):
        return self
