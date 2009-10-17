# -*- coding: utf-8 -*-

from hashlib import md5

import wtforms as forms
from wtforms import validators

from bongo.models import Entry


class EntryForm(forms.Form):
    author = forms.TextField(label=u'autor', validators=[validators.required()])
    text = forms.TextAreaField(label=u'tekst', validators=[validators.required()])

    def save(self):
        e = Entry()
        e['_id'] = md5(self.text.data.encode('utf-8')).hexdigest()
        e.author = self.author.data
        e.text = self.text.data
        e.save()
        return e
