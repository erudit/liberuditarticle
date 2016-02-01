# -*- coding: utf-8 -*-

from django.apps import AppConfig


class EruditArticleConfig(AppConfig):
    name = 'eruditarticle.apps.django_app'
    verbose_name = 'Erudit Article'

    def ready(self):
        from django.conf import settings
        from eruditarticle.conf import set_settings
        set_settings(settings)
