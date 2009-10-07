# -*- coding: utf-8 -*-

from bongo.utils import render_template

def index(request):
    ctx = {}
    return render_template('index.html', **ctx)