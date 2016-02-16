# -*- coding: utf-8 -*-

from .base import EruditBaseObject


class EruditJournal(EruditBaseObject):
    def __init__(self):
        # TODO
        pass


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


class EruditArticle(EruditBaseObject):
    def get_title(self):
        """ Returns the title of the article object. """
        return self.get_text('titre')

    def get_subtitle(self):
        """ Returns the subtitle of the article object. """
        return self.get_text('sstitre')

    def get_full_title(self):
        """ Returns the full title of the article object. """
        title = self.title
        subtitle = self.subtitle

        if title and subtitle:
            return '{0} - {1}'.format(title, subtitle)
        elif title:
            return title
        return None

    title = property(get_title)
    subtitle = property(get_subtitle)
    full_title = property(get_full_title)
