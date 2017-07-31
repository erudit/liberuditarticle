from .base import EruditBaseObject
import collections
import re
import itertools

from .mixins import CopyrightMixin
from .mixins import ISBNMixin
from .mixins import ISSNMixin
from .mixins import PublicationPeriodMixin


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

    def get_publishers(self):
        """ :returns: the publisher of the issue object. """
        return [
            publisher.text
            for publisher in self.findall('editeur//nomorg')
        ]

    def get_editors(self):
        """ :returns: the the editors of the publication object. """
        return self.get_persons('redacteurchef[@typerc="regulier"]')

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
    publishers = property(get_publishers)
