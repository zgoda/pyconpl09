# -*- coding: utf-8 -*-

import datetime
from hashlib import md5

import pymongo
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
        super(Entry, self).save(uuid, validate, safe, *args, **kwargs)

    @classmethod
    def get_latest(cls, num_latest=10):
        return cls.all().sort('date_added', pymongo.DESCENDING).limit(num_latest)

    def get_url(self):
        return u'/%s/' % self._id


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
