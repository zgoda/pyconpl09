# -*- coding: utf-8 -*-

import datetime
from hashlib import md5

import pymongo
from pymongo.dbref import DBRef
import mongokit


class Entry(mongokit.MongoDocument):
    db_name = 'pycon09'
    collection_name = 'entries'
    structure = {
        'text': unicode,
        'author': unicode,
        'date_added': datetime.datetime,
    }
    required_fields = ('author', 'text')
    default_values = {
        'date_added': datetime.datetime.utcnow,
    }
    use_dot_notation = True
    use_autorefs = True
    indexes = [
        {
            'fields': 'date_added',
        },
        {
            'fields': ['text', 'date_added'],
            'unique': True,
        },
    ]

    def save(self, uuid=True, validate=None, safe=True, *args, **kwargs):
        if self.get('_id') is None:
            self['_id'] = md5(self['text'].encode('utf-8')).hexdigest()
        super(Entry, self).save(uuid, validate, safe, *args, **kwargs)

    @classmethod
    def get_latest(cls, num_latest=10):
        return cls.all().sort('date_added', pymongo.DESCENDING).limit(num_latest)

    def get_url(self):
        return u'/%s/' % self._id

    @property
    def next_by_date(self):
        try:
            return list(self.__class__.all({'date_added': {'$gt': self.date_added}}).sort('date_added', pymongo.ASCENDING).limit(1))[0]
        except IndexError:
            return None

    @property
    def prev_by_date(self):
        try:
            return list(self.__class__.all({'date_added': {'$lt': self.date_added}}).sort('date_added', pymongo.DESCENDING).limit(1))[0]
        except IndexError:
            return None

    @property
    def comments(self):
        return Comment.all({'entry': DBRef(self.collection_name, self['_id'])}).sort('date_added', pymongo.DESCENDING)


class Comment(mongokit.MongoDocument):
    db_name = 'pycon09'
    collection_name = 'comments'
    structure = {
        'entry': Entry,
        'text': unicode,
        'author': unicode,
        'date_added': datetime.datetime,
    }
    required_fields = ('entry', 'text', 'author')
    default_values = {
        'date_added': datetime.datetime.utcnow,
    }
    use_dot_notation = True
    use_autorefs = True
    indexes = [
        {
            'fields': ['date_added', 'entry'],
        },
    ]

    def save(self, uuid=True, validate=None, safe=True, *args, **kwargs):
        if self.get('_id') is None:
            self['_id'] = md5('%s-%s' % (self['author'].encode('utf-8'), self['text'].encode('utf-8'))).hexdigest()
        super(Comment, self).save(uuid, validate, safe, *args, **kwargs)
