# -*- coding: utf-8 -*-

import os

from werkzeug import Local, LocalManager
from werkzeug import Response
from werkzeug import import_string
from werkzeug import cached_property
from werkzeug.routing import Map, Rule
from jinja2 import Environment, FileSystemLoader

from bongo import settings


local = Local()
local_manager = LocalManager([local])
application = local('application')

url_map = Map(
    [Rule('/media/<file>', endpoint='media', build_only=True)],
)

def expose(rule, **kw):
    def decorate(f):
        kw['endpoint'] = f.__name__
        url_map.add(Rule(rule, **kw))
        return f
    return decorate

def url_for(endpoint, _external=False, **values):
    return local.url_adapter.build(endpoint, values, force_external=_external)

env = Environment(loader=FileSystemLoader(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'templates')))
env.globals['url_for'] = url_for

def base_context():
    base = {}
    for ctx_name in settings.TEMPLATE_CONTEXT_PROCESSORS:
        ctx_processor = import_string(ctx_name)
        base.update(ctx_processor(local.request))
    return base

def render_template(template, **context):
    ctx = base_context()
    ctx.update(context)
    return Response(env.get_template(template).render(**ctx), mimetype='text/html')


class Pagination(object):

    def __init__(self, objects, per_page, page, endpoint):
        self.objects = objects
        self.per_page = per_page
        self.page = page
        self.endpoint = endpoint

    @cached_property
    def count(self):
        return self.objects.count()

    @cached_property
    def entries(self):
        return self.objects.skip((self.page - 1) * self.per_page).limit(self.per_page)

    has_previous = property(lambda x: x.page > 1)
    has_next = property(lambda x: x.page < x.pages)
    previous = property(lambda x: url_for(x.endpoint, page=x.page - 1))
    next = property(lambda x: url_for(x.endpoint, page=x.page + 1))
    pages = property(lambda x: max(0, x.count - 1) // x.per_page + 1)
