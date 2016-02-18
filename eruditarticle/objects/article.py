# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from ..base import EruditBaseObject


class EruditArticle(EruditBaseObject):
    def get_body(self):
        """ Returns the body of the article object as a Body instance. """
        return Body(self.find('corps'))

    def get_doi(self):
        """ Returns the DOI of the article object. """
        return self.get_text('idpublic[@scheme="doi"]')

    def get_full_title(self):
        """ Returns the full title of the article object. """
        title = self.head.title
        subtitle = self.head.subtitle

        if title and subtitle:
            return '{0} - {1}'.format(title, subtitle)
        elif title:
            return title
        return None

    def get_header(self):
        """ Returns the header of the article object as a Head instance. """
        return Head(self.find('liminaire'))

    body = property(get_body)
    doi = property(get_doi)
    full_title = property(get_full_title)
    header = property(get_header)


class Head(EruditBaseObject):
    def get_abstracts(self):
        """ Returns the abstracts as Abstract instances. """
        abstract_doms = self.findall('resume')
        return [Abstract(adom) for adom in abstract_doms]

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

    def get_title(self):
        """ Returns the title of the article object. """
        return self.get_text('titre')

    def get_subtitle(self):
        """ Returns the subtitle of the article object. """
        return self.get_text('sstitre')

    abstracts = property(get_abstracts)
    authors = property(get_authors)
    title = property(get_title)
    subtitle = property(get_subtitle)


class Abstract(EruditBaseObject):
    def get_content(self):
        """ Returns the content of the abstract. """
        return self.get_text('alinea')

    def get_language(self):
        """ Returns the language code of the abstract. """
        return self._dom.getroot().get('lang')

    content = property(get_content)
    language = property(get_language)


class Body(EruditBaseObject):
    def get_sections(self):
        """ Returns the Section instances associated with the body. """
        sections_doms = self.findall('section1')
        return [Section(sdom, level=1) for sdom in sections_doms]

    sections = property(get_sections)


class Section(EruditBaseObject):
    def __init__(self, xml, level):
        super(Section, self).__init__(xml)
        self.level = level

    def get_title(self):
        return self.get_text('titre')

    title = property(get_title)
