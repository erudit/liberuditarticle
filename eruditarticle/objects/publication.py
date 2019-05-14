try:
    from django.utils.translation import pgettext
    from django.utils.translation import gettext as _
except ImportError:
    pgettext = lambda ctx, msg: msg  # noqa
    _ = lambda x: x  # noqa

import collections
import html
import itertools
import roman
from datetime import datetime

from .base import EruditBaseObject
from .mixins import CopyrightMixin
from .mixins import ISBNMixin
from .mixins import ISSNMixin
from .mixins import PublicationPeriodMixin
from .person import Redacteur, Person, format_authors


class EruditPublication(
    PublicationPeriodMixin, ISBNMixin, ISSNMixin, CopyrightMixin, EruditBaseObject
):
    """
    Expects the ``SUMMARY`` datastream of a Fedora ``Publication`` object
    """
    def get_titles(self, html=True):
        """
        .. warning::
           Will be removed or modified 0.3.0
           For more information please refer to :py:mod:`eruditarticle.objects`

        :returns: the titles of the publication
        """
        return self._get_titles(
            root_elem_name="revue",
            title_elem_name="titrerev",
            subtitle_elem_name="sstitrerev",
            paral_title_elem_name="titrerevparal",
            paral_subtitle_elem_name="sstitrerevparal",
            languages=self.get_languages(),
            html=html,
        )

    def get_languages(self):
        """ :returns: a list of the journal's principal languages, defaults to ['fr']. """
        languages = self.find("revue").get('lang')
        return languages.split() if languages else ['fr']

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
        notes = []
        for note_elem in self.findall('numero/notegen[@typenoteg="edito"]'):

            # If a scope is defined, make sure it's 'numero'.
            scope = note_elem.get('porteenoteg')
            if scope is not None and scope != 'numero':
                continue

            if html:
                parser_method = self.convert_marquage_content_to_html
            else:
                parser_method = self.stringify_children

            alineas_content = parser_method(note_elem, strip_elements=['auteur'])

            authors = [Person(author) for author in note_elem.findall('auteur')]

            note = {
                "lang": note_elem.get("lang"),
                "type": note_elem.get("typenoteg"),
                "content": alineas_content.strip(),
                "authors": format_authors(authors, html=html) if authors else "",
            }
            notes.append(note)

        # Sort the notes according to the journal languages' order.
        languages = self.get_languages()
        notes = sorted(
            notes,
            key=lambda note: languages.index(note['lang']) if note['lang'] in languages else 1
        )

        return notes

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

            themes = redacteurchef.themes
            if themes and theme_id in themes:
                rc.append(redacteurchef)
        return rc

    def _find_themeparal(self, theme_tag, html=False):
        """ Find the parallel names of the theme """
        method = self.get_html if html else self.get_text
        pn = collections.OrderedDict()
        for theme_paral in theme_tag.findall('themeparal'):
            lang = theme_paral.get('lang')
            pn[lang] = {
                'name': method("themeparal[@lang='{}']".format(lang), dom=theme_tag),
                'lang': lang,
                'subname': method("ssthemeparal[@lang='{}']".format(lang), dom=theme_tag),
                'html_name': self.convert_marquage_content_to_html(
                    theme_paral,
                ),
                'html_subname': self.convert_marquage_content_to_html(
                    self.find("ssthemeparal[@lang='{}']".format(lang), dom=theme_tag),
                ),
            }
        return pn

    # TODO fixup the get_theme, get_themes, get_html_themes, get_theme_guest_editors mess
    def parse_theme(self, theme_tag, html=False):
        """ Parse a theme tag """
        method = self.get_html if html else self.get_text
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
        theme['paral'] = self._find_themeparal(theme_tag, html=html)

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
            lambda x: x.format_name(html=True), guest_editors
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
                # Convert html entities (&#201; -> É) so that the first letter gets lowercased.
                subname = html.unescape(subname)
                subname = subname[0].lower() + subname[1:]
            return "{}\xa0: {}".format(name, subname) if subname else name

        return list(map(lambda t: _theme_name_formatter(t[0], t[1], t[2]), theme_name_subnames))

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
            redacteurchef = Redacteur(redacteurchef_tag)
            if formatted:
                redacteurchef_parsed = redacteurchef.format_name(html=html)
            else:
                redacteurchef_parsed = redacteurchef
            redacteurchefs.append(redacteurchef_parsed)
        return redacteurchefs

    def get_html_theme(self):
        """
        .. warning::
           Will be removed or modified 0.3.0
           For more information please refer to :py:mod:`eruditarticle.objects`

        :returns: the theme of the publication object with HTML tags. """
        return self.convert_marquage_content_to_html(self.find('theme'))

    def get_journal_title(self, formatted=False, html=False, subtitles=False):
        """ Return the title of the journal

        :param formatted: if ``True``, format all the parts of the title. Otherwise, return
            a dict containing all the parts.
        :param html:  if ``True``, keep html tags
        :returns: the parts of the journal's title
        """
        titles = self._get_titles(
            root_elem_name='infosommaire/revue',
            title_elem_name='titrerev',
            subtitle_elem_name='sstitrerev',
            paral_title_elem_name='titrerevparal',
            paral_subtitle_elem_name='sstitrerevparal',
            strict_language_check=False,
            html=html
        )

        if not formatted:
            return titles
        else:
            return self._get_formatted_single_title(titles)

    def get_first_page(self):
        """ :returns: the first page of the publication object. """
        roman_pages = []
        arabic_pages = []
        for ppage in self.findall('article//pagination//ppage'):
            if ppage.text is None:
                continue
            try:
                arabic_pages.append(int(ppage.text))
            except ValueError:
                try:
                    roman_pages.append(roman.fromRoman(ppage.text))
                except roman.InvalidRomanNumeralError:
                    pass
        if len(roman_pages):
            return roman.toRoman(min(roman_pages))
        elif len(arabic_pages):
            return str(min(arabic_pages))
        else:
            return None

    def get_last_page(self):
        """ :returns: the last page of the publication object. """
        roman_pages = []
        arabic_pages = []
        for dpage in self.findall('article//pagination//dpage'):
            if dpage.text is None:
                continue
            try:
                arabic_pages.append(int(dpage.text))
            except ValueError:
                try:
                    roman_pages.append(roman.fromRoman(dpage.text))
                except roman.InvalidRomanNumeralError:
                    pass
        if len(arabic_pages):
            return str(max(arabic_pages))
        elif len(roman_pages):
            return roman.toRoman(max(roman_pages))
        else:
            return None

    def get_note_edito(self):
        """ :returns: the edito note associated with the publication object if any. """
        note = self.stringify_children(self.find('notegen[@typenoteg="edito"]'))
        return note.strip() if note is not None else note

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
        return '-'.join([v.text for v in self.findall('numero/volume')
                        if v is not None and v.text is not None])

    def get_number(self):
        """ :returns: the number of the publication object. """
        return '-'.join([n.text for n in self.findall('numero/nonumero')
                        if n is not None and n.text is not None])

    def get_alt_number(self):
        """ :returns: the alternative number of the publication object. """
        return '-'.join([a.text for a in self.findall('numero/anonumero')
                        if a is not None and a.text is not None])

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
        alt_number = self.get_alt_number()
        number_type = self.get_publication_type()
        publication_period = self.get_publication_period()

        if not formatted:
            return {
                'volume': volume,
                'number': number,
                'alt_number': alt_number,
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

        if number and alt_number:
            number = '{} ({})'.format(number, alt_number)
        elif alt_number:
            number = alt_number

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
        elif not volume and not number and publication_period:
            string = "{publication_period}"
        else:
            string = ''
        return string.format(**args)

    article_count = property(get_article_count)
    directors = property(get_directors)
    editors = property(get_editors)
    first_page = property(get_first_page)
    guest_editors = property(get_guest_editors)
    html_theme = property(get_html_theme)
    journal_title = property(get_journal_title)
    last_page = property(get_last_page)
    note_edito = property(get_note_edito)
    production_date = property(get_production_date)
    publication_date = property(get_publication_date)
    publication_year = property(get_publication_year)
    section_titles = property(get_section_titles)
    theme = property(get_theme)
    themes = property(get_themes)
    volume = property(get_volume)
    number = property(get_number)
    alt_number = property(get_alt_number)
    publishers = property(get_publishers)
    languages = property(get_languages)
