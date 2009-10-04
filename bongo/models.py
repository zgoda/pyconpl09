# -*- coding: utf-8 -*-

import datetime

import pymongo
import mongokit


class BlogPost(mongokit.MongoDocument):
    db_name = 'pycon09'
    collection_name = 'blog'
    structure = {
        'title': unicode,
        'text': unicode,
        'author': unicode,
        'date_added': datetime.datetime,
        'pub_date': datetime.datetime,
        'is_draft': bool,
    }
    required_fields = ('title', 'author', 'text')
    default_values = {
        'date_added': datetime.datetime.utcnow,
        'is_draft': False,
    }
    use_dot_notation = True
    indexes = [
        {
            'fields': 'pub_date',
        },
        {
            'fields': ['title', 'pub_date'],
            'unique': True,
        },
    ]

    def save(self, uuid=True, validate=None, safe=True, *args, **kwargs):
        if self.pub_date is None:
            self.is_draft = True
        super(BlogPost, self).save(uuid, validate, safe, *args, **kwargs)

    def get_latest(cls, num_latest=10):
        kw = {
            'is_draft': False,
        }
        cls.all(kw).sort('pub_date', pymongo.DESCENDING)[:num_latest]
