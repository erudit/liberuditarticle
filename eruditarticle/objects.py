# -*- coding: utf-8 -*-
import re
import itertools

from .base import EruditBaseObject
from .mixins import ISBNMixin
from .mixins import ISSNMixin


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


class EruditPublication(ISBNMixin, ISSNMixin, EruditBaseObject):
    def get_article_count(self):
        """ Returns the number of articles of the publication object. """
        return int(self.get_text('nbarticle'))

    def get_directors(self):
        """ Returns the authors of the publication object. """
        return self.get_persons('directeur')

    def get_droitsauteur(self):
        """ Return the list of all copyright notices of this publication.

        The copyrights are returned as a list of the form:

            [
                {'text': 'My copyright', },
                {'href': 'link-url', 'img': 'img-url', },
            ]

        """
        da_list = []
        da_nodes = self.findall('droitsauteur')

        for da in da_nodes:
            link_node = self.find('liensimple', da)
            if link_node:
                da_list.append(self.parse_simple_link(link_node))
            else:
                da_list.append({'text': ''.join(da.itertext())})

        return da_list

    def get_droitsauteurorg(self):
        """ Return the owner of the first copyright for this publication. """
        return self.get_text('droitsauteur/nomorg')

    def get_guest_editors(self):
        """ Returns the guest editors associated with the publication object. """
        return self.get_persons('redacteurchef[@typerc="invite"]')

    def get_notegen_edito(self):
        """ Return the editorial note for this publicaiton """
        notegen = self.get_itertext('notegen[@typenoteg="edito"]')
        return re.sub('^ | $', '', re.sub(' +', ' ', re.sub('\n', '', notegen)))

    def get_notegen_numerique(self):
        """ Return the digital edition note of this publication """
        notegen = self.get_itertext('notegen[@typenoteg="edito"]')
        return re.sub('^ | $', '', re.sub(' +', ' ', re.sub('\n', '', notegen)))

    def get_publication_type(self):
        """ Return the type of this publication """
        return self.get_text('publicationtypecode')

    def _find_journalparal(self, journal_tag, paral_tag_name):
        """ Find the parallel names of the theme """
        pn = {}
        for title_paral in journal_tag.findall(paral_tag_name):
            pn[title_paral.get('lang')] = self.stringify_children(title_paral)
        return pn

    def _find_redacteurchef(self, theme_id):
        """ Find the redacteurchef for the given theme """
        rc = []
        for redacteurchef in self.get_redacteurchef():

            themes = redacteurchef.get('themes')
            if themes and theme_id in themes:
                rc.append(redacteurchef)
        return rc

    def _find_themeparal(self, theme_tag):
        """ Find the parallel names of the theme """
        pn = {}
        for theme_paral in theme_tag.findall('themeparal'):
            pn[theme_paral.get('lang')] = theme_paral.text
        return pn

    def parse_theme(self, theme_tag):
        """ Parse a theme tag """
        theme = {
            'name': self.get_text('theme', dom=theme_tag),
            'subname': self.get_text('sstheme', dom=theme_tag),
        }

        theme_id = theme_tag.get('id')

        # theme redacteurs en chef
        theme['redacteurchef'] = self._find_redacteurchef(theme_id)
        theme['paral'] = self._find_themeparal(theme_tag)

        return theme_id, theme

    def get_themes(self):
        """ Return the themes of this publication """
        themes = {}
        for theme_tag in self.findall('grtheme'):
            theme_id, theme = self.parse_theme(theme_tag)
            themes[theme_id] = theme

        return themes

    def get_redacteurchef(self, idrefs=None):
        """ Return the redacteurchef of this publication """
        tag = 'redacteurchef'
        if idrefs:
            tag = "redacteurchef[@idrefs='{}']".format(idrefs)

        redacteurchefs = []
        redacteurchef_tags = self.findall(tag)
        for redacteurchef_tag in redacteurchef_tags:
            redacteurchef_parsed = self.parse_person(redacteurchef_tag)
            redacteurchef_parsed['type'] = redacteurchef_tag.get('typerc')
            if redacteurchef_tag.get('idrefs'):
                redacteurchef_parsed['themes'] = redacteurchef_tag.get('idrefs').split()
            redacteurchefs.append(redacteurchef_parsed)
        return redacteurchefs

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

    def get_journal_subtitle(self):
        """ Returns the sub-title of the journal associated with the publication object. """
        return self.stringify_children(self.find('revue/sstitrerev'))

    def get_journal_subtitles(self):
        """ Returns all the sub-titles of the journal associated with the publication object. """
        titles = {
            'main': self.journal_subtitle,
            'paral': self._find_journalparal(self.find('revue'), 'sstitrerevparal'),
        }
        return titles

    def get_journal_title(self):
        """ Returns the title of the journal associated with the publication object. """
        return self.stringify_children(self.find('revue/titrerev'))

    def get_journal_titles(self):
        """ Returns all the titles of the journal associated with the publication object. """
        titles = {
            'main': self.journal_title,
            'paral': self._find_journalparal(self.find('revue'), 'titrerevparal'),
        }
        return titles

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

    def get_note_edito(self):
        """ Returns the edito note associated with the publication object if any. """
        note = self.stringify_children(self.find('notegen[@typenoteg="edito"]'))
        return note.strip() if note is not None else note

    def get_note_erudit(self):
        """ Returns the erudit note associated with the publication object if any. """
        note = self.stringify_children(self.find('notegen[@typenoteg="numerique"]'))
        return note.strip() if note is not None else note

    def get_number(self):
        """ Returns the number of the publication object. """
        return self.get_text('nonumero')

    def get_production_date(self):
        """ Returns the production date of the publication object. """
        originator_node = self.find('originator')
        return originator_node.get('date') if originator_node is not None else None

    def get_publication_date(self):
        """ Returns the publication date of the publication object. """
        return self.get_text('numero//pubnum/date')

    def get_publication_period(self):
        """ Returns the publication period of the publication object. """
        year = self.publication_year
        period = self.get_text('numero//pub//periode')
        return ' '.join([period, year]) if period else year

    def get_publication_year(self):
        """ Returns the publication year of the publication object. """
        return self.get_text('numero//pub//annee')

    def get_section_titles(self):
        """ Returns an ordered list of section titles of the publication object. """
        section_titles = []
        for tree_section in self.findall('article//liminaire//grtitre//surtitre'):
            section_titles.append(tree_section.text)
        return [t for t, _ in itertools.groupby(section_titles)]

    def get_theme(self):
        """ Returns the theme of the publication object. """
        return self.stringify_children(self.find('theme'))

    def get_volume(self):
        """ Returns the volume of the publication object. """
        return self.get_text('numero/volume')

    article_count = property(get_article_count)
    directors = property(get_directors)
    droitsauteur = property(get_droitsauteur)
    droitsauteur_org = property(get_droitsauteurorg)
    first_page = property(get_first_page)
    guest_editors = property(get_guest_editors)
    html_theme = property(get_html_theme)
    journal_subtitle = property(get_journal_subtitle)
    journal_subtitles = property(get_journal_subtitles)
    journal_title = property(get_journal_title)
    journal_titles = property(get_journal_titles)
    last_page = property(get_last_page)
    note_edito = property(get_note_edito)
    note_erudit = property(get_note_erudit)
    number = property(get_number)
    production_date = property(get_production_date)
    publication_date = property(get_publication_date)
    publication_period = property(get_publication_period)
    publication_year = property(get_publication_year)
    section_titles = property(get_section_titles)
    theme = property(get_theme)
    volume = property(get_volume)


class EruditArticle(ISBNMixin, ISSNMixin, EruditBaseObject):
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

    def get_ordseq(self):
        """ Returns the ordering number of the article object. """
        return int(self._root.get('ordseq'))

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

    def get_section_title_2(self):
        """ Returns the second section title of the article object. """
        return self.stringify_children(self.find('liminaire//grtitre//surtitre2'))

    def get_section_title_3(self):
        """ Returns the third section title of the article object. """
        return self.stringify_children(self.find('liminaire//grtitre//surtitre3'))

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
    keywords = property(get_keywords)
    lang = property(get_lang)
    last_page = property(get_last_page)
    ordseq = property(get_ordseq)
    processing = property(get_processing)
    publication_year = property(get_publication_year)
    publisher = property(get_publisher)
    section_title = property(get_section_title)
    section_title_2 = property(get_section_title_2)
    section_title_3 = property(get_section_title_3)
    subtitle = property(get_subtitle)
    title = property(get_title)
