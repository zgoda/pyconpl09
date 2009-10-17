# -*- coding: utf-8 -*-

from bongo import settings
from bongo.models import Entry


def site(request):
    return {
        'SITE': settings.SITE,
    }


def latest(request):
    return {
        'LATEST': Entry.get_latest(10),
    }