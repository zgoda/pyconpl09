# -*- coding: utf-8 -*-

import os

from werkzeug import Local, LocalManager
from werkzeug import Response
from werkzeug import import_string
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
