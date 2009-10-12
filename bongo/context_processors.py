# -*- coding: utf-8 -*-

from bongo import settings


def site(request):
    return {
        'SITE': settings.SITE,
    }
