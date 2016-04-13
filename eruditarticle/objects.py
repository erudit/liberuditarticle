# -*- coding: utf-8 -*-

import itertools

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

    def get_first_page(self):
        """ Returns the first page of the publication object. """
        articles = self.findall('article')
        if not len(articles):
            return

        first_article = articles[0]
        try:
            first_page = first_article.find('pagination//ppage').text
        except AttributeError:
            first_page = None

        return first_page

    def get_html_theme(self):
        """ Returns the theme of the publication object with HTML tags. """
        return self.convert_marquage_content_to_html(self.find('theme'))

    def get_last_page(self):
        """ Returns the last page of the publication object. """
        articles = self.findall('article')
        if not len(articles):
            return

        last_article = articles[-1]
        try:
            last_page = last_article.find('pagination//dpage').text
        except AttributeError:
            last_page = None

        return last_page

    def get_number(self):
        """ Returns the number of the publication object. """
        return self.get_text('nonumero')

    def get_publication_period(self):
        """ Returns the publication period of the publication object. """
        year = self.get_text('numero//pub//annee')
        period = self.get_text('numero//pub//periode')
        return ' '.join([period, year]) if period else year

    def get_section_titles(self):
        """ Returns an ordered list of section titles of the publication object. """
        section_titles = []
        for tree_section in self.findall('article//liminaire//grtitre//surtitre'):
            section_titles.append(tree_section.text)
        return [t for t, _ in itertools.groupby(section_titles)]

    def get_theme(self):
        """ Returns the theme of the publication object. """
        return self.stringify_children(self.find('theme'))

    article_count = property(get_article_count)
    directors = property(get_directors)
    first_page = property(get_first_page)
    html_theme = property(get_html_theme)
    last_page = property(get_last_page)
    number = property(get_number)
    publication_period = property(get_publication_period)
    section_titles = property(get_section_titles)
    theme = property(get_theme)


class EruditArticle(EruditBaseObject):
    def get_abstracts(self):
        """ Returns the abstracts of the article object.

        The abstracts are returned as list of dictionaries of the form:

            {
                'lang': 'fr',
                'resume': 'Content',
            }
        """
        abstracts = []
        for tree_abstract in self.findall('resume[@typeresume="resume"]'):
            abstracts.append({
                'lang': tree_abstract.get('lang'),
                'content': self.stringify_children(tree_abstract),
            })
        return abstracts

    def get_article_type(self):
        """ Returns the type of the article. """
        return self._dom.getroot().get('typeart')

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

    def get_html_title(self):
        """ Returns the title of the article object with HTML tags. """
        return self.convert_marquage_content_to_html(self._get_title_element())

    def get_issn(self):
        """ Returns the ISSN number associated with the article object. """
        return self.get_text('revue//idissnnum')

    def get_keywords(self):
        """ Returns the keywords of the article object.

        The keywords are returned as a list of dictionaries of the form:

            {
                'lang': 'fr',
                'keywords': ['foo', 'bar', ],
            }
        """
        keywords = []
        for tree_keywords in self.findall('grmotcle'):
            keywords.append({
                'lang': tree_keywords.get('lang'),
                'keywords': [n.text for n in tree_keywords.findall('motcle')],
            })
        return keywords

    def get_lang(self):
        """ Returns the language of the article object. """
        return self._root.get('lang')

    def get_last_page(self):
        """ Returns the last page of the article object. """
        return self.get_text('infoarticle//pagination//dpage')

    def get_processing(self):
        """ Returns the processing type of the article object. """
        return self._root.get('qualtraitement')

    def get_publication_year(self):
        """ Returns the year of publication of the article object. """
        return self.get_text('numero//pub//annee')

    def get_publisher(self):
        """ Returns the publisher of the article object. """
        return self.get_text('editeur//nomorg')

    def get_section_title(self):
        """ Returns the section title of the article object. """
        return self.stringify_children(self.find('liminaire//grtitre//surtitre'))

    def get_subtitle(self):
        """ Returns the subtitle of the article object. """
        return self.stringify_children(self.find('sstitre'))

    def _get_title_element(self):
        """ Return the element containing the title

        The title element depends on the type of the article """
        element_name = 'titre'
        if self.article_type == 'compterendu':
            element_name = 'trefbiblio'
        return self.find(element_name)

    def get_title(self):
        """ Returns the title of the article object. """
        return self.stringify_children(self._get_title_element())

    abstracts = property(get_abstracts)
    article_type = property(get_article_type)
    authors = property(get_authors)
    doi = property(get_doi)
    first_page = property(get_first_page)
    full_title = property(get_full_title)
    html_title = property(get_html_title)
    issn = property(get_issn)
    keywords = property(get_keywords)
    lang = property(get_lang)
    last_page = property(get_last_page)
    processing = property(get_processing)
    publication_year = property(get_publication_year)
    publisher = property(get_publisher)
    section_title = property(get_section_title)
    subtitle = property(get_subtitle)
    title = property(get_title)
