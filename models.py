# -*- coding: utf-8 -*-

import datetime

from mongokit import MongoDocument as Document


class BlogPost(Document):
    db_name = 'pycon09'
    collection_name = 'blog'
    structure = {
        'title': unicode,
        'text': unicode,
        'author': unicode,
        'date_added': datetime.datetime,
        'pub_date': datetime.datetime,
    }
    required_fields = ('title', 'author', 'text')
    default_values = {
        'date_added': datetime.datetime.utcnow
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

