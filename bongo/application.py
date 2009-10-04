# -*- coding: utf-8 -*-

from werkzeug import Request, ClosingIterator
from werkzeug.exceptions import HTTPException

from bongo.utils import local, local_manager, url_map
from bongo import views


class Bongo(object):

    def __init__(self):
        local.application = self

    def __call__(self, environ, start_response):
        request = Request(environ)
        local.url_adapter = adapter = url_map.bind_to_environ(environ)
        try:
            endpoint, values = adapter.match()
            handler = getattr(views, endpoint)
            response = handler(request, **values)
        except HTTPException, e:
            response = e
        return ClosingIterator(response(environ, start_response), [local_manager.cleanup])
