# -*- coding: utf-8 -*-

from werkzeug import redirect
from werkzeug.exceptions import NotFound
from pymongo.dbref import DBRef

from bongo.utils import expose, render_template
from bongo.models import Entry, Comment
from bongo.forms import EntryForm


@expose('/')
def index(request):
    form = EntryForm(request.form)
    if request.method == 'POST' and form.validate():
        entry = form.save()
        return redirect(entry.get_url())
    entries = Entry.get_latest()
    ctx = {
        'form': form,
        'entries': entries,
        'num_entries': entries.count(),
    }
    return render_template('index.html', **ctx)


@expose('/<entry_id>/')
def entry(request, entry_id):
    entry = Entry.one({'_id': entry_id})
    if not entry:
        raise NotFound
    comments = Comment.all({'entry': DBRef('entries', entry_id)})
    ctx = {
        'entry': entry,
        'comments': comments,
        'num_comments': comments.count(),
    }
    return render_template('entry.html', **ctx)
