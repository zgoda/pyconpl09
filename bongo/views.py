# -*- coding: utf-8 -*-

from werkzeug import redirect
from werkzeug.exceptions import NotFound
import pymongo

from bongo.utils import expose, render_template, Pagination
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


@expose('/mysli/', defaults={'page': 1})
@expose('/mysli/<int:page>/')
def entries(request, page):
    entries = Entry.all().sort('date_added', pymongo.ASCENDING)
    pagination = Pagination(entries, 20, page, 'entries')
    if pagination.page > 1 and not pagination.entries:
        raise NotFound()
    ctx = {
        'pagination': pagination,
    }
    return render_template('entries.html', **ctx)


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
        raise NotFound()
    form = CommentForm(request.form)
    if request.method == 'POST' and form.validate():
        form.save(entry)
        return redirect(entry.get_url())
    ctx = {
        'entry': entry,
        'form': form,
    }
    return render_template('entry.html', **ctx)
