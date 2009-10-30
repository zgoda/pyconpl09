# -*- coding: utf-8 -*-

import os

from werkzeug import Request, ClosingIterator, SharedDataMiddleware
from werkzeug import import_string
from werkzeug.exceptions import HTTPException
from werkzeug.contrib.sessions import SessionMiddleware

from bongo.utils import local, local_manager, url_map
from bongo import views
from bongo import settings


class Bongo(object):

    def __init__(self):
        local.application = self
        storage_class = import_string(settings.SESSION_STORE)
        if not os.path.isdir(settings.SESSION_PATH):
            os.makedirs(settings.SESSION_PATH)
        self.dispatch = SessionMiddleware(self.dispatch, storage_class(path=settings.SESSION_PATH))
        self.dispatch = SharedDataMiddleware(self.dispatch, {
            '/media': settings.MEDIA_ROOT,
        })

    def __call__(self, environ, start_response):
        return self.dispatch(environ, start_response)

    def dispatch(self, environ, start_response):
        local.request = request = Request(environ)
        response = None
        for request_processor_name in settings.REQUEST_PROCESSORS:
            processor = import_string(request_processor_name)()
            response = processor.process_request(request)
            if response is not None:
                break
        if response is None:
            local.url_adapter = adapter = url_map.bind_to_environ(environ)
            try:
                endpoint, values = adapter.match()
                handler = getattr(views, endpoint)
                response = handler(request, **values)
                for request_processor_name in reversed(settings.REQUEST_PROCESSORS):
                    processor = import_string(request_processor_name)()
                    response = processor.process_response(request, response)
            except HTTPException, e:
                response = e
        return ClosingIterator(response(environ, start_response), [local_manager.cleanup])
