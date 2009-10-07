# -*- coding: utf-8 -*-

import wtforms as forms
from wtforms import validators

from bongo.models import Entry


class EntryForm(forms.Form):
    author = forms.TextField(label=u'autor', validators=[validators.required()])
    text = forms.TextAreaField(label=u'tekst', validators=[validators.required()])

    def save(self):
        e = Entry()
        e.author = self.author.data
        e.text = self.text.data
        e.save()
        return e
