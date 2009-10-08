# -*- coding: utf-8 -*-

import os

from werkzeug import Request, ClosingIterator, SharedDataMiddleware
from werkzeug.exceptions import HTTPException

from bongo.utils import local, local_manager, url_map
from bongo import views


class Bongo(object):

    def __init__(self):
        local.application = self
        self.dispatch = SharedDataMiddleware(self.dispatch, {
            '/media': os.path.join(os.path.abspath(os.path.dirname(__file__)), 'media'),
        })

    def __call__(self, environ, start_response):
        return self.dispatch(environ, start_response)

    def dispatch(self, environ, start_response):
        request = Request(environ)
        local.url_adapter = adapter = url_map.bind_to_environ(environ)
        try:
            endpoint, values = adapter.match()
            handler = getattr(views, endpoint)
            response = handler(request, **values)
        except HTTPException, e:
            response = e
        return ClosingIterator(response(environ, start_response), [local_manager.cleanup])
