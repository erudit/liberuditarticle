import collections
from copy import copy

import lxml.etree as et
import six

from ..utils import remove_xml_namespaces, normalize_whitespace
from .dom import DomObject
from .person import Person

Title = collections.namedtuple('Title', ['title', 'subtitle', 'lang'])


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

    def _format_single_title(self, title):
        """ format a Title namedtuple """
        if title.title[-1] in '.!?':
            separator = ' '
        else:
            if title.lang == "fr":
                separator = "\xa0: "
            else:
                separator = ": "
        if title.title and title.subtitle:
            return "{title}{separator}{subtitle}".format(
                title=title.title,
                separator=separator,
                subtitle=title.subtitle[:1].lower() + title.subtitle[1:]
                if ':' in separator else title.subtitle,
            )
        return "{title}".format(
            title=title.title
        )

    def _get_formatted_single_title(self, titles, use_equivalent=False):
        """ Format the main, paral and equivalent titles in a single title

            :param use_equivalent: whether or not to use equivalent titles. In the
                case of formatting an :py:class:`erudit.models.Article` title, only
                paralel titles are used. The XML of :py:class:`erudit.models.Journal`
                equivalent titles are also used.

            :returns: a formatted title
        """

        sections = []
        if titles['main'].title is not None:
            sections.append(self._format_single_title(titles['main']))

        if titles['paral']:
            sections.append(" / ".join(
                self._format_single_title(paral_title)
                for paral_title in titles['paral']
            ))

        if titles['equivalent'] and use_equivalent:
            sections.append(" / ".join(
                self._format_single_title(paral_title)
                for paral_title in titles['equivalent']
            ))

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
            raise ValueError

        titles = {
            'main': None,
            'paral': [],
            'equivalent': [],
        }

        paral_titles = self.find_paral(
            root_elem,
            paral_title_elem_name,
            html=html,
        )

        paral_subtitles = self.find_paral(
            root_elem,
            paral_subtitle_elem_name,
            html=html,
        )

        # Process the paral and equivalent titles first since they have a 'lang' attribute and the
        # main title does not.
        for lang, title in paral_titles.items():
            paral_title = Title(
                title=title,
                lang=lang,
                subtitle=paral_subtitles[lang] if lang in paral_subtitles else None
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

        if html:
            parser_method = self.convert_marquage_content_to_html
        else:
            parser_method = self.stringify_children

        strip_elements = ['liensimple', 'renvoi']

        titles['main'] = Title(
            title=parser_method(title_elem, strip_elements),
            subtitle=parser_method(subtitle_elem, strip_elements),
            lang=languages.pop(0) if languages else 'fr'
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

    def stringify_children(self, node, strip_elements=None):
        """ Convert a node content to string

        :param strip_elements: elements to strip before converting to string

        :returns: the text embedded in a specific node by stripping all tags
            and stripping specified elements.
        """
        if node is None:
            return None
        node = copy(node)
        if strip_elements:
            et.strip_elements(node, *strip_elements, with_tail=False)
        et.strip_tags(node, "*")
        if node.text is not None:
            return normalize_whitespace(node.text)

    def find_paral(self, tag, paral_tag_name, html=True):
        """ Find the parallel values for the given tag using the given tag name. """
        pn = collections.OrderedDict()
        for title_paral in tag.findall(paral_tag_name):
            if html:
                pn[title_paral.get('lang')] = self.convert_marquage_content_to_html(title_paral)
            else:
                pn[title_paral.get('lang')] = self.stringify_children(title_paral)
        return pn
