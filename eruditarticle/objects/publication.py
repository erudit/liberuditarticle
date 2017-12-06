try:
    from django.utils.translation import pgettext
    from django.utils.translation import gettext as _
except ImportError:
    pgettext = lambda ctx, msg: msg  # noqa
    _ = lambda x: x  # noqa

import collections
import re
import itertools
from datetime import datetime

from .base import EruditBaseObject
from .mixins import CopyrightMixin
from .mixins import ISBNMixin
from .mixins import ISSNMixin
from .mixins import PublicationPeriodMixin


class EruditPublication(
    PublicationPeriodMixin, ISBNMixin, ISSNMixin, CopyrightMixin, EruditBaseObject
):
    """
    Expects the ``SUMMARY`` datastream of a Fedora ``Publication`` object
    """
    def get_titles(self, strip_markup=False):
        """
        .. warning::
           Will be removed or modified 0.3.0
           For more information please refer to :py:mod:`eruditarticle.objects`

        :returns: the titles of the publication

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

    def get_notegens_edito(self, formatted=False, html=False):
        """ Return the editorial note for this publication

        .. note::
           XML markup is partially supported. Author names are not converted to HTML.

        :param html: convert XML markup to HTML
        :returns: a list of notegens
        """
        first_article = self.find('article')
        notes = []
        for note_elem in self.findall('notegen[@typenoteg="edito"]', dom=first_article):

            if html:
                parser_method = self.convert_marquage_content_to_html
            else:
                parser_method = self.stringify_children

            alineas_content = parser_method(note_elem)
            alineas_content = re.sub('^ | $', '', re.sub(' +', ' ', re.sub('\n', '', alineas_content)))  # noqa

            note = {
                "lang": note_elem.get("lang"),
                "type": note_elem.get("typenoteg"),
                "content": alineas_content
            }
            notes.append(note)
        return notes

    def get_notegen_numerique(self):
        """ Return the digital edition note of this publication """
        notegen = self.get_itertext('notegen[@typenoteg="edito"]')
        return re.sub('^ | $', '', re.sub(' +', ' ', re.sub('\n', '', notegen)))

    def get_publication_type(self, formatted=False):
        """ Return the type of this publication

        Return the ``publicationtypecode`` of the Publication object.

        :param formatted: if False, only the publication type code will be returned
        :returns:
        """
        publication_type = self.get_text('publicationtypecode')
        if formatted:
            if publication_type == 'supp':
                return pgettext("numbering", 'supplément')
            if publication_type == 'index':
                return pgettext("numbering", 'index')
            if publication_type == 'hs':
                return pgettext("numbering", 'hors-série')
        else:
            return publication_type

    def _find_redacteurchef(self, theme_id, html=False):
        """ Find the redacteurchef for the given theme """
        rc = []
        for redacteurchef in self.get_redacteurchef(html=html):

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
                ),
                'html_subname': self.convert_marquage_content_to_html(
                    self.find("ssthemeparal[@lang='{}']".format(lang), dom=theme_tag),
                ),
            }
        return pn

    def parse_theme(self, theme_tag, html=False):
        """ Parse a theme tag """

        method = self.get_text
        if html:
            method = self.get_html

        theme = {
            'name': method('theme', dom=theme_tag),
            'lang': self.find('theme').get('lang') or "fr",
            'subname': method('sstheme', dom=theme_tag),
            'html_name': self.convert_marquage_content_to_html(
                self.find('theme', dom=theme_tag),
            ),
            'html_subname': self.convert_marquage_content_to_html(
                self.find('sstheme', dom=theme_tag),
            ),
        }
        theme_id = theme_tag.get('id')
        # theme redacteurs en chef
        theme['redacteurchef'] = self._find_redacteurchef(theme_id, html=html)
        theme['paral'] = self._find_themeparal(theme_tag)

        return theme_id, theme

    def get_themes(self, html=False, formatted=False):
        """ :returns: the themes of this publication """
        themes = collections.OrderedDict()
        for theme_tag in self.findall('grtheme'):
            theme_id, theme = self.parse_theme(theme_tag, html=html)
            themes[theme_id] = theme
        if formatted:
            formatted_themes = []
            for theme_id, theme in themes.items():
                formatted_themes.append(
                    {
                        'names': self._format_theme_names(theme),
                        'editors': self.get_formatted_theme_guest_editors(theme)
                    }
                )
            return formatted_themes
        return themes

    def get_formatted_theme_guest_editors(self, theme):
        """
        .. warning::
           Will be removed or modified 0.3.0
           For more information please refer to :py:mod:`eruditarticle.objects`

        Format the names of the guest editors of the theme """
        guest_editors = theme.get("redacteurchef", [])
        formatted_guest_editors = map(
            lambda x: self.format_person_name(x, html=True), guest_editors
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
        """
        .. warning::
           Will be removed or modified 0.3.0
           For more information please refer to :py:mod:`eruditarticle.objects`

        :returns: the formatted themes of this publication """
        return self.get_themes(html=True, formatted=True)

    def get_redacteurchef(self, typerc=None, idrefs=None, formatted=False, html=False):
        """
        Return the list of redacteurchef of this Publication. If called with the default arguments,
        ``get_redacteurchef`` will return a list containg all redacteurchef objects of this
        publication.

        :param typerc:
            If specified, only return redacteurchef matching that type. Must be one of "regulier"
            or "invite"
        :param idrefs: Filter redacteurchef by theme id.
            Value of ``idrefs`` must be one of the following:

            :None: all redacteurchef, whether they are linked to a theme or
              not, will be returned.
            :list[str]: only redacteurchef linked to these themes will be returned.
            :[]: only redacteurchef linked to **NO** themes will be returned

        :param boolean formatted: format the redacteurchef name
        :param boolean html: if set to True, html tags will be kept
        :type idrefs: list[str] or None
        :type typerc: str or None
        :raises ValueError: if typerc is not one of "regulier" or "invite"
        :returns: a list of redacteurchef objects of this publication """

        tag = 'redacteurchef'

        if typerc is not None and typerc not in ["regulier", "invite"]:
            raise ValueError("Must be 'regulier' or 'invite'")

        attribute_search = []
        if idrefs is not None and len(idrefs) == 0:
            attribute_search.append("not(@idrefs)")
        elif idrefs is not None:
            idrefs_search = []
            for idref in idrefs:
                idrefs_search.append('contains(@idrefs, "{}")'.format(idref))
            idrefs_query = "({})".format(" or ".join(idrefs_search))
            attribute_search.append(idrefs_query)
        if typerc:
            attribute_search.append("@typerc='{}'".format(typerc))

        if attribute_search:
            tag = "redacteurchef[{}]".format(
                " and ".join(attribute_search)
            )

        redacteurchefs = []
        redacteurchef_tags = self._root.xpath("//{}".format(tag))
        for redacteurchef_tag in redacteurchef_tags:
            if formatted:
                redacteurchef_parsed = self.format_person_name(
                    self.parse_person(redacteurchef_tag),
                    html=html
                )
            else:
                redacteurchef_parsed = self.parse_person(redacteurchef_tag, html=html)
                redacteurchef_parsed['typerc'] = redacteurchef_tag.get('typerc')
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
        """
        .. warning::
           Will be removed or modified 0.3.0
           For more information please refer to :py:mod:`eruditarticle.objects`

        :returns: the theme of the publication object with HTML tags. """
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

    def get_publication_date(self, as_datetime=False):
        """ Return the publication date
        :param as_datetime: return a datetime object. Assumes that the
        date is formatted as %Y-%m-%d

        :returns: the publication date of the publication object.
        """
        publication_date = self.get_text("numero//pubnum/date")
        if not as_datetime:
            return publication_date
        else:
            return datetime.strptime(publication_date, "%Y-%m-%d")

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

    def get_volume_numbering(self, html=False, abbreviated=False, formatted=False):
        """ Return the volume title of this publication

        If not formatted, return a dictionary containg the volume
        numbering information for this publication.

        If formatted, format the result as a locale aware string.

        :param html: return result as HTML
        :param abbreviated: if the formatted result should be abbreviated.
            Only has effect if ``formatted=True``.
        :param formatted: format the result as a String

        :returns: the volume title of this publication
        """

        volume = self.get_volume()
        number = self.get_number()
        number_type = self.get_publication_type()
        publication_period = self.get_publication_period()

        if not formatted:
            return {
                'volume': volume,
                'number': number,
                'number_type': number_type,
                'publication_period': publication_period
            }

        if abbreviated and html:
            volume_str = pgettext('numbering', "Vol.")
            number_str = pgettext('numbering', "N<sup>o</sup>")
            untranslated_number_str = "N<sup>o</sup>"
        elif abbreviated:
            volume_str = pgettext('numbering', "Vol.")
            number_str = pgettext('numbering', "N°")
            untranslated_number_str = "N°"
        else:
            volume_str = pgettext('numbering', "Volume")
            number_str = pgettext('numbering', "Numéro")
            untranslated_number_str = "Numéro"

        if number_type == 'hs':
            number_type = self.get_publication_type(formatted=True)
            number_str_number_type = pgettext(
                "numbering", "{} hors-série".format(untranslated_number_str)
            )
        else:
            number_type = self.get_publication_type(formatted=True)
            number_str_number_type = pgettext("numbering", "{} {}".format(
                untranslated_number_str, number_type
            ))

        args = dict(
            volume=volume,
            number=number,
            number_type=number_type,
            number_type_lcase=number_type.lower() if number_type else None,
            publication_period=publication_period,
            publication_period_lcase=publication_period.lower() if publication_period else None,
            number_str=number_str,
            number_str_lcase=number_str.lower() if number_str else None,
            volume_str=volume_str,
            number_str_number_type=number_str_number_type,
            number_str_number_type_lcase = number_str_number_type.lower() if number_str_number_type else None  # noqa
        )

        if volume and number and number_type:
            string = _('{volume_str} {volume}, {number_str_lcase} {number}, {number_type_lcase}, {publication_period_lcase}')  # noqa
        elif volume and not number and number_type:
            string = _('{volume_str} {volume}, {number_str_number_type_lcase}, {publication_period_lcase}')  # noqa
        elif volume and number:
            string = _('{volume_str} {volume}, {number_str_lcase} {number}, {publication_period_lcase}')  # noqa
        elif volume and not number:
            string = _('{volume_str} {volume}, {publication_period_lcase}')
        elif not volume and number and number_type:
            string = _('{number_str} {number}, {number_type_lcase}, {publication_period_lcase}')
        elif not volume and number_type and number_type.lower() == 'index':
            string = _('Index, {publication_period_lcase}')
        elif not volume and not number and number_type:
            string = _('{number_str_number_type}, {publication_period_lcase}')
        elif not volume and number:
            string = _('{number_str} {number}, {publication_period_lcase}')
        return string.format(**args)

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
