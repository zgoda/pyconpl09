# -*- coding: utf-8 -*-

from werkzeug import redirect
from werkzeug.exceptions import NotFound

from bongo.utils import expose, render_template
from bongo.models import Entry
from bongo.forms import EntryForm, CommentForm


@expose('/')
def index(request):
    form = EntryForm(request.form)
    entries = Entry.get_latest()
    ctx = {
        'form': form,
        'entries': entries,
        'num_entries': entries.count(),
    }
    return render_template('index.html', **ctx)


@expose('/dodaj/')
def add_entry(request):
    form = EntryForm(request.form)
    if request.method == 'POST' and form.validate():
        entry = form.save()
        return redirect(entry.get_url())
    ctx = {
        'form': form
    }
    return render_template('add_entry_form.html', **ctx)


@expose('/e/<entry_id>/')
def entry(request, entry_id):
    entry = Entry.one({'_id': entry_id})
    if not entry:
        raise NotFound
    form = CommentForm(request.form)
    if request.method == 'POST' and form.validate():
        form.save(entry)
        return redirect(entry.get_url())
    ctx = {
        'entry': entry,
        'form': form,
    }
    return render_template('entry.html', **ctx)
