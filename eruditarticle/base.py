# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import lxml.etree as et
import six

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
        dom = dom if dom is not None else self._dom
        return dom.find('.//{}'.format(tag_name))

    def findall(self, tag_name, dom=None):
        """ Find elements in the tree. """
        dom = dom if dom is not None else self._dom
        return dom.findall('.//{}'.format(tag_name))

    def get_text(self, tag_name, dom=None):
        """ Returns the text associated with the considered tag. """
        result = self.find(tag_name, dom=dom)
        return result.text if result is not None else None

    def get_text_from_tags(self, tag_names, dom=None):
        """ Returns the first text value associated with a list of potential tags. """
        text = None
        for tname in tag_names:
            text = self.get_text(tname, dom=dom)
            if text:
                break
        return text
