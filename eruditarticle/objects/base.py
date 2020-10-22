import collections

import lxml.etree as et
import re
import six

from ..utils import remove_xml_namespaces
from .dom import DomObject
from .person import Person
from .exceptions import MissingXMLElementError


class Title:

    STRIP_ELEMENTS = ['renvoi']

    def __init__(self, title=None, subtitle=None, lang=None, html=True):
        if html:
            parser_method = EruditBaseObject.convert_marquage_content_to_html
        else:
            parser_method = EruditBaseObject.stringify_children
        self.title = parser_method(title, strip_elements=self.STRIP_ELEMENTS)
        self.subtitle = parser_method(subtitle, strip_elements=self.STRIP_ELEMENTS)
        self.lang = lang
        self.xml_title = et.tostring(title) if title is not None else None
        self.xml_subtitle = et.tostring(subtitle) if subtitle is not None else None

    def __repr__(self):
        return 'Title(title="{}", subtitle="{}", lang="{}")'.format(
            self.title,
            self.subtitle,
            self.lang,
        )

    def __eq__(self, other):
        return str(self) == str(other)

    def format(self, with_subtitle=True):
        """ Format a title with or without its subtitle. """
        # If we don't ask for the subtitle or if there is no subtitle, just return the title.
        if not with_subtitle or not self.subtitle:
            return self.title

        title = self.title
        subtitle = self.subtitle

        # Check if the title ends with a punctuation, with or without a marquage ending tag.
        punctuation_match = re.search(
            r'[\.\!\?](?:<\/marquage>)?<\/[a-z]+>$',
            self.xml_title.decode().strip()
        )
        # If the title ends with a punctuation, do not add a colon before the subtitle.
        if punctuation_match:
            separator = ' '
        # For French titles, add a non-breaking space and a colon before the subtitle.
        elif self.lang == "fr":
            separator = "\xa0: "
        # Otherwise, add a colon before the subtitle.
        else:
            separator = ": "

        # Check if uppercase is forced on the subtitle.
        uppercase_match = re.search(
            r'^<[a-z]+><marquage typemarq=\"majuscule\">',
            self.xml_subtitle.decode().strip()
        )
        # Lowercase French subtitles if following a colon and uppercase is not forced.
        if self.lang == "fr" and ':' in separator and not uppercase_match:
            subtitle = subtitle[:1].lower() + subtitle[1:]

        return "{title}{separator}{subtitle}".format(
            title=title,
            separator=separator,
            subtitle=subtitle,
        )


class EruditBaseObject(DomObject):
    def __init__(self, xml):
        if isinstance(xml, six.string_types) or isinstance(xml, six.moves.builtins.bytes):
            self._dom = remove_xml_namespaces(et.fromstring(xml))
        else:
            self._dom = remove_xml_namespaces(xml)
        super().__init__(self._dom.getroot())

    def __getattr__(self, name):
        try:
            val = super(EruditBaseObject, self).__getattr__(name)
        except AttributeError:
            pass
        else:
            return val

        # Tries to fetch the value of the tag whose name
        # matches the considered attribute
        result = self.find(name)
        if result is None:
            raise AttributeError

        return result

    def _get_formatted_single_title(self, titles, use_equivalent=False, subtitles=True):
        """ Format the main, paral and equivalent titles in a single title

            :param use_equivalent: whether or not to use equivalent titles. In the
                case of formatting an :py:class:`erudit.models.Article` title, only
                paralel titles are used. The XML of :py:class:`erudit.models.Journal`
                equivalent titles are also used.

            :returns: a formatted title
        """

        sections = []
        if titles['main'].title is not None:
            sections.append(titles['main'].format(with_subtitle=subtitles))

        paral_titles = []
        for paral_title in titles['paral']:
            # Format parallel title.
            formatted_paral_title = paral_title.format(with_subtitle=subtitles)
            # Add the parallel title to the list only if it's different than the main title.
            if formatted_paral_title not in sections:
                paral_titles.append(formatted_paral_title)
        # Add parallel titles to the main title.
        if paral_titles:
            sections.append(' / '.join(paral_titles))

        if use_equivalent:
            equivalent_titles = []
            for equivalent_title in titles['equivalent']:
                # Format equivalent title.
                formatted_equivalent_title = equivalent_title.format(with_subtitle=subtitles)
                # Add the equivalent title to the list only if it's different than the main title.
                if formatted_equivalent_title not in sections:
                    equivalent_titles.append(formatted_equivalent_title)
            # Add equivalent titles to the main title.
            if equivalent_titles:
                sections.append(' / '.join(equivalent_titles))

        return " / ".join(sections)

    def _get_titles(
        self, root_elem_name=None, title_elem_name=None, subtitle_elem_name=None,
        paral_title_elem_name=None, paral_subtitle_elem_name=None, languages=['fr'],
        strict_language_check=True, html=True
    ):
        """ Helper method to extract titles relative to a root element

        This supports retrieving article object titles and journal object titles.

        For a complete description of the behaviour see :meth:`objects.ArticleObject.get_titles`

        :param root_elem_name: the root element
        :param title_elem_name: name of title element
        :param subtitle_elem_name: name of the subtitle element
        :param paral_title_elem_name: name of the parallel subtitle element
        :param paral_subtitle_elem_name: name of the parallel subtitle element
        :param strict_language_check: Determine whether or not to check if the title language
            is one of the official document languages. If set to ``True``, only titles with a
            language specified in the ``language`` iterable will be considered ``paral`` titles,
            with the other titles being considered equivalent.
        :param languages: official languages of the document. Defaults to ``['fr']``.

        :returns: the titles and subtitles relative to ``root_elem_name``
        """
        root_elem = self.find(root_elem_name)

        if root_elem is None:
            raise MissingXMLElementError(root_elem_name)

        titles = {
            'main': None,
            'paral': [],
            'equivalent': [],
        }

        paral_titles = self.find_paral(
            root_elem,
            paral_title_elem_name,
        )

        paral_subtitles = self.find_paral(
            root_elem,
            paral_subtitle_elem_name,
        )

        # Process the paral and equivalent titles first since they have a 'lang' attribute and the
        # main title does not.
        for lang, title in paral_titles.items():
            if title.text is None:
                continue
            paral_title = Title(
                title=title,
                subtitle=paral_subtitles[lang] if lang in paral_subtitles else None,
                lang=lang,
                html=html,
            )

            if not strict_language_check or lang in languages:
                titles['paral'].append(paral_title)
                if lang in languages:
                    languages.remove(lang)
            else:
                titles['equivalent'].append(paral_title)

        title_elem = self.find(title_elem_name, dom=root_elem)
        subtitle_elem = self.find(subtitle_elem_name, dom=root_elem)

        # Set title_elem to None if it has no text and no child
        if title_elem is None or (not title_elem.text and len(title_elem) == 0):
            title_elem = None

        titles['main'] = Title(
            title=title_elem,
            subtitle=subtitle_elem,
            lang=languages.pop(0) if languages else 'fr',
            html=html,
        )
        return titles

    def parse_simple_link(self, simplelink_node):
        """ Parses a "liensimple" node.

        :returns: a dictionary of the form::

            { 'href': '[link]', 'img': '[link]', }

        """
        link = {
            'href': simplelink_node.get('href'),
        }

        image_node = self.find('objetmedia//image', simplelink_node)
        if image_node is not None:
            link.update({'img': image_node.get('href')})

        return link

    def get_persons(self, tag_name, dom=None, html=False, formatted=False):
        """
        .. warning::
           Will be removed or modified 0.3.0
           For more information please refer to :py:mod:`eruditarticle.objects`

        :returns: the persons for the considered tag name.

        Return a list of Person
        """
        persons = []
        for tree_author in self.findall(tag_name):
            persons.append(Person(tree_author))
        return persons

    def find_paral(self, tag, paral_tag_name):
        """ Find the parallel values for the given tag using the given tag name. """
        pn = collections.OrderedDict()
        for title_paral in tag.findall(paral_tag_name):
            pn[title_paral.get('lang')] = title_paral
        return pn
