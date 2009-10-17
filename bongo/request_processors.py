# -*- coding: utf-8 -*-


class RequestProcessor(object):

    def process_request(self, request):
        pass

    def process_response(self, request, response):
        return response


class SessionRequestProcessor(RequestProcessor):

    def process_request(self, request):
        session = request.environ.get('werkzeug.session')
        request.session = session
