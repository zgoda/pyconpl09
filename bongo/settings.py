# -*- coding: utf-8 -*-

SITE = {
    'name': u'Mongo-Bongo',
    'domain': u'localhost:5000',
}

TEMPLATE_CONTEXT_PROCESSORS = (
    'bongo.context_processors.site',
)

REQUEST_PROCESSORS = ()