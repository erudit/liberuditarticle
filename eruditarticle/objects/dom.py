from copy import copy

import lxml.etree as et

from .. import xslt
from ..utils import normalize_whitespace


class DomObject:
    def __init__(self, root):
        assert root is not None
        self._root = root

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

    def get_html(self, tag_name, dom=None):
        """ :returns: the content of the considered tag converted to html. """
        result = self.find(tag_name, dom=dom)
        return self.convert_marquage_content_to_html(result)

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

    def strip_markup(self):
        et.strip_tags(self._root, 'marquage')

    @staticmethod
    def convert_marquage_content_to_html(node, strip_elements=['renvoi']):
        """ Converts <marquage> tags to HTML using a specific node.

        :param strip_elements: (list, optional): Defaults to ['renvoi'].
            A list of XML elements to strip from the node.
            By default we strip 'renvoi' tags because the XSLT now support the conversion of
            'renvoi' tags to footnote links. This was required to allow footnotes in abstracts, but
            we don't want those footnotes elsewhere since they were previously ignored by the XSLT.
        :returns: the node's text as a string with the converted html.
        """
        if node is None:
            return
        node = copy(node)
        if strip_elements:
            et.strip_elements(node, *strip_elements, with_tail=False)
        # Converts <marquage> tags to HTML
        _node = xslt.marquage_to_html(node)
        # Strip all other tags but keep text
        et.strip_tags(
            _node,
            *[
                node.tag, 'caracunicode', 'citation', 'equationligne', 'exposant', 'indice',
                'liensimple', 'marquepage', 'objetmedia', 'renvoi'
            ])
        _html = et.tostring(_node.getroot(), method='html')
        output = _html.split(b'>', 1)[1].rsplit(b'<', 1)[0]
        return normalize_whitespace(output.decode('utf-8'))
