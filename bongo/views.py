# -*- coding: utf-8 -*-

from werkzeug import redirect
from werkzeug.exceptions import NotFound

from bongo.utils import expose, render_template
from bongo.models import Entry
from bongo.forms import EntryForm


@expose('/')
def index(request):
    form = EntryForm(request.form)
    if request.method == 'POST' and form.validate():
        entry = form.save()
        return redirect(entry.get_url())
    ctx = {
        'form': form,
        'entries': list(Entry.get_latest()),
    }
    return render_template('index.html', **ctx)


@expose('/<entry_id>/')
def entry(request, entry_id):
    entry = Entry.one({'_id': entry_id})
    if not entry:
        raise NotFound
    ctx = {
        'entry': entry,
    }
    return render_template('entry.html', **ctx)
