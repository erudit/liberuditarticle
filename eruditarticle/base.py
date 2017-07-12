# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import collections
from copy import copy
import re

import lxml.etree as et
import six

from . import xslt
from .utils import remove_xml_namespaces

Title = collections.namedtuple('Title', ['title', 'subtitle', 'lang'])


class EruditBaseObject(object):
    def __init__(self, xml):
        if isinstance(xml, six.string_types) or isinstance(xml, six.moves.builtins.bytes):
            self._dom = remove_xml_namespaces(et.fromstring(xml))
        else:
            self._dom = remove_xml_namespaces(xml)
        self._root = self._dom.getroot()

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

    def find(self, tag_name, dom=None):
        """ Find an element in the tree. """
        dom = dom if dom is not None else self._root
        return dom.find('.//{}'.format(tag_name))

    def findall(self, tag_name, dom=None):
        """ Find elements in the tree. """
        dom = dom if dom is not None else self._root
        return dom.findall('.//{}'.format(tag_name))

    def get_nodes(self, dom=None):
        """ :returns: all the elements under the current root. """
        dom = dom if dom is not None else self._root
        return dom.xpath('child::node()')

    def get_text(self, tag_name, dom=None):
        """ :returns: the text associated with the considered tag. """
        result = self.find(tag_name, dom=dom)
        return result.text if result is not None else None

    def get_itertext(self, tag_name, dom=None):
        """ :returns: the text associated with the considered tag and its children tags
        """
        result = self.find(tag_name, dom=dom)
        return "".join(result.itertext()) if result is not None else None

    def get_text_from_tags(self, tag_names, dom=None):
        """ :returns: the first text value associated with a list of potential tags. """
        text = None
        for tname in tag_names:
            text = self.get_text(tname, dom=dom)
            if text:
                break
        return text

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
        paral_title_elem_name=None, paral_subtitle_elem_name=None, languages=None,
        strip_markup=False
    ):
        """ Helper method to extract titles relative to a root element

        This supports retrieving article object titles and journal object titles.

        For a complete description of the behaviour see :meth:`objects.ArticleObject.get_titles`

        :param root_elem_name: the root element
        :param title_elem_name: name of title element
        :param subtitle_elem_name: name of the subtitle element
        :param paral_title_elem_name: name of the parallel subtitle element
        :param paral_subtitle_elem_name: name of the parallel subtitle element

        :returns: the titles and subtitles relative to ``root_elem_name``
        """
        root_elem = self.find(root_elem_name)

        if root_elem is None:
            raise ValueError

        if not languages:
            languages = ['fr']

        title_elem = self.find(title_elem_name, dom=root_elem)

        # Set title_elem to None if it has no text and no child
        if title_elem is None or (not title_elem.text and len(title_elem) == 0):
            title_elem = None

        subtitle_elem = self.find(subtitle_elem_name, dom=root_elem)
        if strip_markup:
            title = Title(
                title=self.stringify_children(title_elem) if title_elem is not None else None,
                subtitle=self.stringify_children(subtitle_elem),
                lang=languages.pop(0)
            )
        else:
            title = Title(
                title=self.convert_marquage_content_to_html(
                    title_elem if title_elem is not None else None,
                    as_string=True
                ),
                subtitle=self.convert_marquage_content_to_html(
                    subtitle_elem,
                    as_string=True
                ),
                lang=languages.pop(0)
            )

        titles = {
            'main': title,
            'paral': [],
            'equivalent': [],
        }

        paral_titles = self.find_paral(
            root_elem,
            paral_title_elem_name,
            strip_markup=strip_markup
        )

        paral_subtitles = self.find_paral(
            root_elem,
            paral_subtitle_elem_name,
            strip_markup=strip_markup
        )

        for lang, title in paral_titles.items():
            paral_title = Title(
                title=title,
                lang=lang,
                subtitle=paral_subtitles[lang] if lang in paral_subtitles else None
            )

            if lang in languages:
                titles['paral'].append(paral_title)
            else:
                titles['equivalent'].append(paral_title)
        return titles

    def format_person_name(self, person):
        """ Formats the name in the person dictionary

        :returns: the formatted person name
        """

        formatted_person_name = ""

        keys_order = ['prefix', 'firstname', 'othername', 'lastname', 'suffix']

        first_item = True
        for index, key in enumerate(keys_order):
            if key in person and person[key]:
                if first_item:
                    value = ""
                    first_item = False
                else:
                    value = " "
                formatted_person_name += value + person[key]

        if 'pseudo' in person:
            return formatted_person_name + ', alias ' + self.format_person_name(person['pseudo'])

        return formatted_person_name

    def parse_person(self, person_tag):
        """ Parses a person tag

        :returns: a person dictionary

        The persons are returned as a list of dictionaries of the form::

            [
                {
                   'firstname': 'Foo',
                   'lastname': 'Bar',
                   'othername': 'Dummy',
                   'affiliations': ['TEST1', 'TEST2']
                   'email': 'foo.bar@example.com',
                   'organization': 'Test',
                   'suffix': 'Ph.D.'
                },
            ]
        """
        et.strip_tags(person_tag, 'marquage')

        person = {
            'firstname': self.get_text('prenom', dom=person_tag),
            'lastname': self.get_text('nomfamille', dom=person_tag),
            'othername': self.get_text('autreprenom', dom=person_tag),
            'suffix': self.get_text('suffixe', dom=person_tag),
            'affiliations': [
                self.get_text('alinea', dom=affiliation_dom)
                for affiliation_dom in self.findall('affiliation', dom=person_tag)
            ],
            'email': self.get_text('courriel/liensimple', dom=person_tag),
            'organization': self.get_text('nomorg', dom=person_tag),
            'role': {},
        }

        find_role = et.XPath('fonction')
        roles = find_role(person_tag)
        for role in roles:
            person['role'][role.get('lang')] = role.text

        pseudo = self.find('nompers[@typenompers="pseudonyme"]', dom=person_tag)
        all_person_names = self.findall('nompers', dom=person_tag)
        if pseudo and len(all_person_names) > 1:
            person['pseudo'] = self.parse_person(pseudo)
        return person

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

    def get_persons(self, tag_name, dom=None):
        """ :returns: the persons for the considered tag name.

        Return a list of dictionaries in the format specified by parse_person
        """
        persons = []
        for tree_author in self.findall(tag_name):
            persons.append(self.parse_person(tree_author))
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
            return re.sub(' +', ' ', node.text)

    def convert_marquage_content_to_html(self, node, as_string=False, strip_elements=None):
        """ Converts <marquage> tags to HTML using a specific node.

            :param as_string: encode the bytes as an utf-8 string
        """
        if node is None:
            return
        if strip_elements:
            et.strip_elements(node, *strip_elements, with_tail=False)
        # Converts <marquage> tags to HTML
        _node = xslt.marquage_to_html(copy(node))
        # Strip all other tags but keep text
        et.strip_tags(
            _node,
            *[
                node.tag, 'caracunicode', 'citation', 'equationligne', 'exposant', 'indice',
                'liensimple', 'marquepage', 'objetmedia', 'renvoi'
            ])
        _html = et.tostring(_node.getroot())
        output = _html.split(b'>', 1)[1].rsplit(b'<', 1)[0]
        if output and as_string:
            return output.decode('utf-8')
        return output

    def find_paral(self, tag, paral_tag_name, strip_markup=False):
        """ Find the parallel values for the given tag using the given tag name. """
        pn = collections.OrderedDict()
        for title_paral in tag.findall(paral_tag_name):
            if strip_markup:
                pn[title_paral.get('lang')] = self.stringify_children(title_paral)
            else:
                pn[title_paral.get('lang')] = self.convert_marquage_content_to_html(
                    title_paral, as_string=True
                )
        return pn
