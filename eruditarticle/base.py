# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from copy import copy

import lxml.etree as et
import six

from . import xslt
from .utils import remove_xml_namespaces


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
        """ Returns all the elements under the current root. """
        dom = dom if dom is not None else self._root
        return dom.xpath('child::node()')

    def get_text(self, tag_name, dom=None):
        """ Returns the text associated with the considered tag. """
        result = self.find(tag_name, dom=dom)
        return result.text if result is not None else None

    def get_itertext(self, tag_name, dom=None):
        """ Returns the text associated with the considered tag and
its children tags """
        result = self.find(tag_name, dom=dom)
        return "".join(result.itertext()) if result is not None else None

    def get_text_from_tags(self, tag_names, dom=None):
        """ Returns the first text value associated with a list of potential tags. """
        text = None
        for tname in tag_names:
            text = self.get_text(tname, dom=dom)
            if text:
                break
        return text

    def parse_person(self, person_tag):
        """ Parses a person tag

        Returns a dictionary in the form:
        The persons are returned as a list of dictionaries of the form:

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
        return {
            'firstname': self.get_text('prenom', dom=person_tag),
            'lastname': self.get_text('nomfamille', dom=person_tag),
            'othername': self.get_text('autreprenom', dom=person_tag),
            'affiliations': [
                self.get_text('alinea', dom=affiliation_dom)
                for affiliation_dom in self.findall('affiliation', dom=person_tag)
            ],
            'email': self.get_text('courriel/liensimple', dom=person_tag)
        }

    def parse_simple_link(self, simplelink_node):
        """ Parses a "liensimple" node.

        Returns a dictionary of the form:

            {
                'href': '[link]',
                'img': '[link]',
            }

        """
        link = {
            'href': simplelink_node.get('href'),
        }

        image_node = self.find('objetmedia//image', simplelink_node)
        if image_node is not None:
            link.update({'img': image_node.get('href')})

        return link

    def get_persons(self, tag_name, dom=None):
        """ Returns the persons for the considered tag name.

        Return a list of dictionaries in the format specified by parse_person
        """
        persons = []
        for tree_author in self.findall(tag_name):
            persons.append(self.parse_person(tree_author))
        return persons

    def stringify_children(self, node):
        """ Returns the text embedded in a specific node by removing any tags. """
        try:
            return ''.join([x for x in node.itertext()])
        except AttributeError:
            return

    def convert_marquage_content_to_html(self, node):
        """ Converts <marquage> tags to HTML using a specific node. """
        # Converts <marquage> tags to HTML
        _node = xslt.marquage_to_html(copy(node))
        # Strip all other tags but keep text
        et.strip_tags(
            _node,
            *[
                node.tag, 'caracunicode', 'citation', 'equationligne', 'exposant', 'indice',
                'liensimple', 'marquepage', 'objetmedia',
            ])
        _html = et.tostring(_node.getroot())
        return _html.split(b'>', 1)[1].rsplit(b'<', 1)[0]

    def find_paral(self, tag, paral_tag_name):
        """ Find the parallel values for the given tag using the given tag name. """
        pn = {}
        for title_paral in tag.findall(paral_tag_name):
            pn[title_paral.get('lang')] = self.stringify_children(title_paral)
        return pn
