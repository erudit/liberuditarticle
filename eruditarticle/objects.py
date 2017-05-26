# -*- coding: utf-8 -*-

import collections
import re
import itertools

from .base import EruditBaseObject
from .mixins import CopyrightMixin
from .mixins import ISBNMixin
from .mixins import ISSNMixin
from .mixins import PublicationPeriodMixin


class EruditJournal(EruditBaseObject):

    def get_title(self):
        """ :returns: the title of the journal """
        return self.find('setName').text

    def get_first_publication_year(self):
        """ :returns: the first publication year of the journal. """
        pubyears = self.get_publication_years()
        return pubyears[0] if pubyears else None

    def get_last_publication_year(self):
        """ :returns: the last publication year of the journal. """
        pubyears = self.get_publication_years()
        return pubyears[-1] if pubyears else None

    def get_publication_period(self):
        """ :returns: the publication period of the journal object. """
        pubyears = self.get_publication_years()
        years_count = len(pubyears)
        if years_count > 1:
            return '{} - {}'.format(pubyears[0], pubyears[-1])
        elif years_count:
            return pubyears[0]

    def get_publication_years(self):
        """ :returns: the publication period of the journal object. """
        pubyears = []
        for tree_year in self.findall('annee'):
            pubyears.append(tree_year.get('valeur'))
        pubyears = sorted(pubyears)
        return pubyears

    first_publication_year = property(get_first_publication_year)
    last_publication_year = property(get_last_publication_year)
    publication_period = property(get_publication_period)


class EruditPublication(
    PublicationPeriodMixin, ISBNMixin, ISSNMixin, CopyrightMixin, EruditBaseObject
):
    def get_titles(self, strip_markup=False):
        """ :returns: the titles of the publication

        If the publication does not specify a principal language, it is assumed
        to be French.
        """
        languages = self.find("revue").get('lang')
        if languages:
            languages = languages.split()
        else:
            languages = ["fr"]
        return self._get_titles(
            root_elem_name="revue",
            title_elem_name="titrerev",
            subtitle_elem_name="sstitrerev",
            paral_title_elem_name="titrerevparal",
            paral_subtitle_elem_name="sstitrerevparal",
            languages=languages,
            strip_markup=strip_markup
        )

    def get_article_count(self):
        """ :returns: the number of articles of the publication object. """
        return int(self.get_text('nbarticle'))

    def get_directors(self):
        """ :returns: the authors of the publication object. """
        return self.get_persons('directeur')

    def get_editors(self):
        """ :returns: the the editors of the publication object. """
        return self.get_persons('redacteurchef')

    def get_guest_editors(self):
        """ :returns: the guest editors associated with the publication object. """
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
        pn = collections.OrderedDict()
        for theme_paral in theme_tag.findall('themeparal'):
            lang = theme_paral.get('lang')
            pn[lang] = {
                'name': theme_paral.text,
                'subname': self.get_text("ssthemeparal[@lang='{}']".format(lang), dom=theme_tag),
                'html_name': self.convert_marquage_content_to_html(
                    theme_paral,
                    as_string=True
                ),
                'html_subname': self.convert_marquage_content_to_html(
                    self.find("ssthemeparal[@lang='{}']".format(lang), dom=theme_tag),
                    as_string=True
                ),
            }
        return pn

    def parse_theme(self, theme_tag):
        """ Parse a theme tag """
        theme = {
            'name': self.get_text('theme', dom=theme_tag),
            'lang': self.find('theme').get('lang') or "fr",
            'subname': self.get_text('sstheme', dom=theme_tag),
            'html_name': self.convert_marquage_content_to_html(
                self.find('theme', dom=theme_tag),
                as_string=True
            ),
            'html_subname': self.convert_marquage_content_to_html(
                self.find('sstheme', dom=theme_tag),
                as_string=True
            ),
        }
        theme_id = theme_tag.get('id')

        # theme redacteurs en chef
        theme['redacteurchef'] = self._find_redacteurchef(theme_id)
        theme['paral'] = self._find_themeparal(theme_tag)

        return theme_id, theme

    def get_themes(self):
        """ Return the themes of this publication """
        themes = collections.OrderedDict()
        for theme_tag in self.findall('grtheme'):
            theme_id, theme = self.parse_theme(theme_tag)
            themes[theme_id] = theme
        return themes

    def get_formatted_theme_guest_editors(self, theme):
        """ Format the names of the guest editors of the theme """
        guest_editors = theme.get("redacteurchef", [])
        formatted_guest_editors = map(
            lambda x: self.format_person_name(x), guest_editors
        )
        return list(formatted_guest_editors)

    def _format_theme_names(self, theme):
        """ Format the theme name """
        theme_name_subnames = [
            (theme['name'], theme.get('subname', None), theme['lang'])
        ] + [
            (paral['name'], paral.get('subname', None), paral.get('lang'))
            for paral in theme['paral'].values()
        ]

        def _theme_name_formatter(name, subname, lang):
            # Lower case the first letter if theme name is in French.
            if subname and lang == 'fr':
                subname = subname[0].lower() + subname[1:]
            return "{} : {}".format(name, subname) if subname else name

        return list(map(lambda t: _theme_name_formatter(t[0], t[1], t[2]), theme_name_subnames))

    def get_formatted_themes(self):
        """ Return the formatted themes of this publication """
        themes = self.get_themes()
        formatted_themes = []
        for theme_id, theme in themes.items():
            formatted_themes.append(
                {
                    'names': self._format_theme_names(theme),
                    'editors': self.get_formatted_theme_guest_editors(theme)
                }
            )
        return formatted_themes

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
        """ :returns: the first page of the publication object. """
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
        """ :returns: the theme of the publication object with HTML tags. """
        return self.convert_marquage_content_to_html(self.find('theme'))

    def get_journal_subtitle(self):
        """ :returns: the sub-title of the journal associated with the publication object. """
        return self.stringify_children(self.find('revue/sstitrerev'))

    def get_journal_subtitles(self):
        """ :returns: all the sub-titles of the journal associated with the publication object. """
        titles = {
            'main': self.journal_subtitle,
            'paral': self.find_paral(self.find('revue'), 'sstitrerevparal'),
        }
        return titles

    def get_journal_title(self):
        """ :returns: the title of the journal associated with the publication object. """
        return self.stringify_children(self.find('revue/titrerev'))

    def get_journal_titles(self):
        """ :returns: all the titles of the journal associated with the publication object. """
        titles = {
            'main': self.journal_title,
            'paral': self.find_paral(self.find('revue'), 'titrerevparal'),
        }
        return titles

    def get_last_page(self):
        """ :returns: the last page of the publication object. """
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
        """ :returns: the edito note associated with the publication object if any. """
        note = self.stringify_children(self.find('notegen[@typenoteg="edito"]'))
        return note.strip() if note is not None else note

    def get_note_erudit(self):
        """ :returns: the erudit note associated with the publication object if any. """
        note = self.stringify_children(self.find('notegen[@typenoteg="numerique"]'))
        return note.strip() if note is not None else note

    def get_number(self):
        """ :returns: the number of the publication object. """
        nonumero_nodes = self.findall('nonumero')
        return '-'.join([n.text for n in nonumero_nodes])

    def get_production_date(self):
        """ :returns: the production date of the publication object. """
        originator_node = self.find('originator')
        return originator_node.get('date') if originator_node is not None else None

    def get_publication_date(self):
        """ :returns: the publication date of the publication object. """
        return self.get_text('numero//pubnum/date')

    def get_publication_year(self):
        """ :returns: the publication year of the publication object. """
        return self.get_text('numero//pub//annee')

    def get_section_titles(self):
        """ :returns: an ordered list of section titles of the publication object. """
        section_titles = []
        for tree_section in self.findall('article//liminaire//grtitre//surtitre'):
            section_titles.append(tree_section.text)
        return [t for t, _ in itertools.groupby(section_titles)]

    def get_theme(self):
        """ :returns: the theme of the publication object. """
        return self.stringify_children(self.find('theme'))

    def get_volume(self):
        """ :returns: the volume of the publication object. """
        return self.get_text('numero/volume')

    article_count = property(get_article_count)
    directors = property(get_directors)
    editors = property(get_editors)
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
    publication_year = property(get_publication_year)
    section_titles = property(get_section_titles)
    theme = property(get_theme)
    themes = property(get_themes)
    volume = property(get_volume)


class EruditArticle(PublicationPeriodMixin, ISBNMixin, ISSNMixin, CopyrightMixin, EruditBaseObject):
    def get_abstracts(self):
        """ :returns: the abstracts of the article object.

        The abstracts are returned as list of dictionaries of the form::

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
        """ :returns: the type of the article. """
        return self._dom.getroot().get('typeart')

    def get_authors(self):
        """ :returns: the authors of the article object. """
        authors = [
            self.parse_person(author) for author in
            self._root.xpath('//auteur[not(contribution[@typecontrib!="aut"])]')
        ]
        return authors

    def get_formatted_authors(self):
        """ :returns: the formatted author names of the article object. """
        return [
            self.format_person_name(author)
            for author in self.get_authors()
        ]

    def get_notegens(self):
        """ :returns: the notes of the article object. """
        notegen_nodes = self.findall('notegen')
        notegens = []
        for notegen_node in notegen_nodes:
            notegen = {}
            alinea_nodes = self.findall("alinea", dom=notegen_node)
            notegen['type'] = notegen_node.get('typenoteg')
            notegen["content"] = [
                self.convert_marquage_content_to_html(n, as_string=True)
                for n in alinea_nodes
            ]

            notegens.append(notegen)
        return notegens

    def get_doi(self):
        """ :returns: the DOI of the article object. """
        return self.get_text('idpublic[@scheme="doi"]')

    def get_first_page(self):
        """ :returns: the first page of the article object. """
        return self.get_text('infoarticle//pagination//ppage')

    def get_html_body(self):
        """ :returns: the full body of the article object as HTML text. """
        alinea_nodes = self.findall('para/alinea')
        if alinea_nodes:
            html_body = b' '.join([self.convert_marquage_content_to_html(n) for n in alinea_nodes])
        else:
            texte_node = self.find('corps/texte')
            html_body = self.convert_marquage_content_to_html(texte_node)
        return b' '.join(html_body.split()) if html_body else ''

    def get_html_title(self):
        """ :returns: the title of the article object with HTML tags. """
        return self.convert_marquage_content_to_html(self.find('titre'))

    def get_keywords(self):
        """ :returns: the keywords of the article object.

        The keywords are returned as a list of dictionaries of the form::

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

    def get_languages(self):
        """ :returns: the language of the article object. """
        return self._root.get('lang').split()

    def get_language(self):
        """ Return the principal language of the article. """
        languages = self.get_languages()
        if languages:
            return languages[0]

    def get_last_page(self):
        """ :returns: the last page of the article object. """
        return self.get_text('infoarticle//pagination//dpage')

    def get_ordseq(self):
        """ :returns: the ordering number of the article object. """
        ordseq = self._root.get('ordseq')
        return int(ordseq) if ordseq is not None else 0

    def get_processing(self):
        """ :returns: the processing type of the article object. """
        return self._root.get('qualtraitement')

    def get_publication_year(self):
        """ :returns: the year of publication of the article object. """
        return self.get_text('numero//pub//annee')

    def get_publisher(self):
        """ :returns: the publisher of the article object. """
        return self.get_text('editeur//nomorg')

    def get_section_titles(self, level=1, html=True):
        """ :returns: the section titles of the article object

            :param title_type: type of the title (main or paral)
            :param level: level of the section title (1, 2 or 3)
            :param html: True if special characters should be converted to html entities
        """
        if level not in (1, 2, 3):
            raise ValueError("Level should be 1, 2 or 3")

        section_title = self._get_section_title(level=level)

        surtitre_elem = 'surtitreparal{}'.format(
            "" if level == 1 else level
        )

        return {
            'main': section_title,
            'paral': self.find_paral(self.find('liminaire//grtitre'), surtitre_elem),
        } if section_title else None

    def _get_section_title(self, level=1):
        """ :returns: the section title of the article object. """
        element = 'liminaire//grtitre//surtitre{}'.format(
            "" if level == 1 else level
        )

        return self.convert_marquage_content_to_html(
            self.find(element),
            as_string=True
        )

    def get_subtitle(self):
        """ :returns: the subtitle of the article object. """
        return self.stringify_children(self.find('sstitre'))

    def _get_reviewed_or_referenced_works(self, tag, strip_markup=False):
        if not strip_markup:
            references = [
                self.convert_marquage_content_to_html(ref, as_string=True).strip()
                for ref in self.findall(tag)
            ]
        else:
            references = [
                self.stringify_children(ref).strip()
                for ref in self.findall(tag)
            ]
        return references

    def get_reviewed_works(self, strip_markup=False):
        """ :returns: the works reviewed by this article """
        return self._get_reviewed_or_referenced_works('trefbiblio', strip_markup=strip_markup)

    def get_references(self, strip_markup=False):
        """ :returns: the works referenced by this article. returns a dictionary
                that contains possibly two keys: doi and title

            :param strip_markup: strip all xml markup
        """
        references = []
        xml_references = self.findall('refbiblio')
        for reference in xml_references:
            doi = reference.find('idpublic[@scheme="doi"]')
            if doi is not None:
                doi = doi.text
            if strip_markup:
                title = self.stringify_children(reference, strip_elements=('idpublic',))
            else:
                title = self.convert_marquage_content_to_html(
                    reference, as_string=True, strip_elements=('idpublic',)
                )
            references.append({'doi': doi, 'title': title})
        return references

    def get_title(self):
        """ :returns: the title of the article object. """
        return self.stringify_children(
            self.find('titre', dom=self.find('grtitre')),
            strip_elements=['liensimple', 'renvoi']
        )

    def get_journal_titles(self):
        """ :returns: the titles of the journal

        This method has the same behaviour as :meth:`~.get_titles`.
        """
        languages = self.find('revue').get('lang').split()
        return self._get_titles(
            root_elem_name='revue',
            title_elem_name='titrerev',
            subtitle_elem_name='sstitrerev',
            paral_title_elem_name='titrerevparal',
            paral_subtitle_elem_name='sstitrerevparal',
            languages=languages,
        )

    def get_titles(self, strip_markup=False):
        """ Retrieve the titles of an article

        :param strip_markup: if set to True, strip all XML / HTML markup and return only
            a string.

        :returns: a dict containing all the titles and subtitles of the object.

        Titles are grouped in four categories: ``main``, ``paral``, ``equivalent`` and
        ``reviewed_works``, where  ``main`` is the title proper, ``paral`` the
        parallel titles proper, and ``equivalent`` the original titles in a language
        different from that of the title proper. Parallel titles accompanies an article
        body in the specified language, while equivalent titles do not have an
        accompanying article body.

        The value for ``main`` is an Title namedtuple. The value for ``paral`` and
        ``equivalent`` is a list of Title namedtuples. The value for
        ``reviewed_works`` is a list of strings. Items in ``paral`` are ordered
        by the position of their ``lang`` attribute in the main ``<article>``. Items in
        ``equivalent`` are ordered by their position in the XML document.

        Here is an example of a return value::

            titles = {
                'main': Title(
                    title='Serge Emmanuel Jongué',
                    subtitle='Capter et narrer l'indicible',
                    lang='fr',
                },
                'paral': [
                    Title(
                        title='Serge Emmanuel Jongué',
                        subtitle='Capturing and Narrating the Unspeakable',
                        lang='en'
                    )
                ],
                'equivalent': [
                    Title(
                    title='la lorem ipsum dolor sit amet',
                    subtitle='la sub lorem ipsum',
                    lang='es',
                ],
                reviewed_works=[],
            }

        While the ``lang`` attribute of each ``<titreparal>`` tag is specified explicitely,
        the ``lang`` of the main title is not specified in the XML document. It is assumed
        to be the first value of ``lang`` in the ``<article>`` tag.

        If the article is ill-defined and specifies a subtitle for a given language without
        specifying a corresponding title, this subtitle will be ignored.

        Ref: http://www.erudit.org/xsd/article/3.0.0/doc/eruditarticle_xsd.html#article

        """

        titles = self._get_titles(
            root_elem_name='grtitre',
            title_elem_name='titre',
            subtitle_elem_name='sstitre',
            paral_title_elem_name='titreparal',
            paral_subtitle_elem_name='sstitreparal',
            languages=self.get_languages(),
            strip_markup=strip_markup
        )

        titles['reviewed_works'] = self.get_reviewed_works(strip_markup=strip_markup)
        return titles

    def _format_single_title(self, title):
        """ format an Title namedtuple """
        if title.lang == "fr":
            separator = " :\xa0"
        else:
            separator = " : "
        if title.title and title.subtitle:
            return "{title}{separator}{subtitle}".format(
                title=title.title,
                separator=separator,
                subtitle=title.subtitle
            )
        return "{title}".format(
            title=title.title
        )

    def get_formatted_journal_title(self):
        """ Format the journal title

        :returns: the formatted journal title

        Calls :meth:~.get_journal_titles` and format its results.
        """
        titles = self.get_journal_titles()
        return self._get_formatted_single_title(titles, use_equivalent=True)

    def _get_formatted_title(self, strip_markup=False):
        """ Format the article titles

        :returns: the formatted article title

        This method calls :meth:`~.get_titles` and format its results.

        The result is formatted in the following way::

            "{main_title} : {main_subtitle} / .. /  {paral_title_n} : {paral_subtitle_n} / {reviewed_works}"  # noqa

        If an article title is in French, a non-breaking space is inserted after the colon
        separating it from its subtitle.
        """
        titles = self.get_titles(strip_markup=strip_markup)
        formatted_title = self._get_formatted_single_title(titles)

        if titles['reviewed_works']:
            reviewed_works = " / ".join(
                reference for reference in titles['reviewed_works']
            )

            if formatted_title:
                formatted_title = "{title} / {reviewed_works}".format(
                    title=formatted_title,
                    reviewed_works=reviewed_works
                )
            else:
                formatted_title = reviewed_works
        return formatted_title

    def get_formatted_title(self):
        return self._get_formatted_title(strip_markup=True)

    def get_formatted_html_title(self):
        return self._get_formatted_title(strip_markup=False)

    abstracts = property(get_abstracts)
    article_type = property(get_article_type)
    authors = property(get_authors)
    reviewed_works = property(get_reviewed_works)
    doi = property(get_doi)
    first_page = property(get_first_page)
    html_body = property(get_html_body)
    html_title = property(get_html_title)
    keywords = property(get_keywords)
    languages = property(get_languages)
    language = property(get_language)
    last_page = property(get_last_page)
    ordseq = property(get_ordseq)
    processing = property(get_processing)
    publication_year = property(get_publication_year)
    publisher = property(get_publisher)
    subtitle = property(get_subtitle)
    title = property(get_title)
    titles = property(get_titles)
