# -*- coding: utf-8 -*-

from .base import EruditBaseObject


class EruditJournal(EruditBaseObject):
    def __init__(self, *args, **kwargs):
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
    def get_authors(self):
        """ Returns the authors of the article object.

        The authors are returned as a list of dictionaries of the form:

            [
                {
                   'firstname': 'Foo',
                   'lastname': 'Bar',
                   'othername': 'Dummy',
                   'affiliations': ['TEST1', 'TEST2']
                   'email': 'foo.bar@example.com',
                },
            ]
        """
        authors = []
        for tree_author in self.findall('auteur'):
            authors.append({
                'firstname': self.get_text('prenom', dom=tree_author),
                'lastname': self.get_text('nomfamille', dom=tree_author),
                'othername': self.get_text('autreprenom', dom=tree_author),
                'affiliations': [
                    self.get_text('alinea', dom=affiliation_dom)
                    for affiliation_dom in self.findall('affiliation', dom=tree_author)],
                'email': self.get_text('courriel/liensimple', dom=tree_author),
            })
        return authors

    def get_doi(self):
        """ Returns the DOI of the article object. """
        return self.get_text('idpublic[@scheme="doi"]')

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

    authors = property(get_authors)
    doi = property(get_doi)
    title = property(get_title)
    subtitle = property(get_subtitle)
    full_title = property(get_full_title)
