# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from ..base import EruditBaseObject


class EruditPublication(EruditBaseObject):
    def get_article_count(self):
        """ Returns the number of articles of the publication object. """
        return int(self.get_text('nbarticle'))

    def get_number(self):
        """ Returns the number of the publication object. """
        return self.get_text('nonumero')

    def get_theme(self):
        """ Returns the theme of the publication object. """
        return self.get_text('theme')

    article_count = property(get_article_count)
    number = property(get_number)
    theme = property(get_theme)
