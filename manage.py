#!/usr/bin/env python
# -*- coding: utf-8 -*-

from werkzeug import script


def make_app():
    from bongo.application import Bongo
    return Bongo()

def make_shell():
    from bongo import models, utils
    application = make_app()
    return locals()


action_runserver = script.make_runserver(make_app, use_reloader=True)
action_shell = script.make_shell(make_shell)

script.run()
