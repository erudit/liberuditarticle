# -*- coding: utf-8 -*-


class DisableMigrations(object):
    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return 'notmigrations'


INSTALLED_APPS = (
    'eruditarticle',
)

LANGUAGE_CODE = "fr"
SECRET_KEY = "secret"
