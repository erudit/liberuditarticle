# -*- coding: utf-8 -*-

from .base import EruditBaseObject


class EruditJournal(EruditBaseObject):
    # TODO
    pass


class EruditPublication(EruditBaseObject):
    # TODO
    pass


class EruditArticle(EruditBaseObject):
    def get_title(self):
        """Returns the title of the article object."""
        return self.get_text('titre')

    def get_subtitle(self):
        """Returns the subtitle of the article object."""
        return self.get_text('sstitre')

    def get_full_title(self):
        """Returns the full title of the article object."""
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
