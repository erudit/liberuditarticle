from copy import copy

import lxml.etree as et

from .. import xslt


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

    @staticmethod
    def convert_marquage_content_to_html(node, strip_elements=None):
        """ Converts <marquage> tags to HTML using a specific node.
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
        return output.decode('utf-8')