# -*- coding: utf-8 -*-

from .base import EruditBaseObject


class EruditJournal(EruditBaseObject):
    def get_publication_period(self):
        """ Returns the publication period of the journal object. """
        pubyears = []
        for tree_year in self.findall('annee'):
            pubyears.append(int(tree_year.get('valeur')))
        pubyears = sorted(pubyears)

        years_count = len(pubyears)
        if years_count > 1:
            return '{} - {}'.format(pubyears[0], pubyears[-1])
        elif years_count:
            return pubyears[0]

    publication_period = property(get_publication_period)


class EruditPublication(EruditBaseObject):
    def get_article_count(self):
        """ Returns the number of articles of the publication object. """
        return int(self.get_text('nbarticle'))

    def get_directors(self):
        """ Returns the authors of the publication object. """
        return self.get_persons('directeur')

    def get_number(self):
        """ Returns the number of the publication object. """
        return self.get_text('nonumero')

    def get_theme(self):
        """ Returns the theme of the publication object. """
        return self.get_text('theme')

    article_count = property(get_article_count)
    directors = property(get_directors)
    number = property(get_number)
    theme = property(get_theme)


class EruditArticle(EruditBaseObject):
    def get_authors(self):
        """ Returns the authors of the article object. """
        return self.get_persons('auteur')

    def get_doi(self):
        """ Returns the DOI of the article object. """
        return self.get_text('idpublic[@scheme="doi"]')

    def get_first_page(self):
        """ Returns the first page of the article object. """
        return self.get_text('infoarticle//pagination//ppage')

    def get_full_title(self):
        """ Returns the full title of the article object. """
        title = self.title
        subtitle = self.subtitle

        if title and subtitle:
            return '{0} - {1}'.format(title, subtitle)
        elif title:
            return title
        return None

    def get_lang(self):
        """ Returns the language of the article object. """
        return self._root.get('lang')

    def get_last_page(self):
        """ Returns the last page of the article object. """
        return self.get_text('infoarticle//pagination//dpage')

    def get_processing(self):
        """ Returns the processing type of the article object. """
        return self._root.get('qualtraitement')

    def get_subtitle(self):
        """ Returns the subtitle of the article object. """
        return self.get_text('sstitre')

    def get_title(self):
        """ Returns the title of the article object. """
        return self.get_text('titre')

    authors = property(get_authors)
    doi = property(get_doi)
    first_page = property(get_first_page)
    full_title = property(get_full_title)
    lang = property(get_lang)
    last_page = property(get_last_page)
    processing = property(get_processing)
    subtitle = property(get_subtitle)
    title = property(get_title)
