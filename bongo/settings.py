# -*- coding: utf-8 -*-

import os


SESSION_STORE = 'werkzeug.contrib.sessions.FilesystemSessionStore'
SESSION_PATH = os.path.join(os.environ['HOME'], 'var', 'sessiondata')

SITE = {
    'name': u'Mongo-Bongo',
    'domain': u'localhost:5000',
}

TEMPLATE_CONTEXT_PROCESSORS = (
    'bongo.context_processors.site',
    'bongo.context_processors.latest',
)

REQUEST_PROCESSORS = (
    'bongo.request_processors.SessionRequestProcessor',
)