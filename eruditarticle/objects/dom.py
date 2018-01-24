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


class DomPersonName(DomObject):
    def format(self, html=False):
        get = self.get_html if html else self.get_text
        keys_order = ['prenom', 'autreprenom', 'nomfamille', 'suffixe']
        ordered_vals = [get(key) for key in keys_order]
        return ' '.join(v for v in ordered_vals if v)


class DomPerson(DomObject):
    # NOTE: This is one of the slowest parts of liberuditarticle.
    #
    # Searching for slow tests and profiling the code led to discover that this
    # function was a bottleneck. When asking for a "html" person, a XSL transfo
    # is performed for every tag. An optimization would be to perform *one*
    # XSL transformation for the whole sub tree.
    @property
    def firstname(self):
        return self.get_text('prenom')

    @property
    def lastname(self):
        return self.get_text('nomfamille')

    @property
    def othername(self):
        return self.get_text('autreprenom')

    @property
    def suffix(self):
        return self.get_text('suffixe')

    @property
    def email(self):
        return self.get_text('courriel/liensimple')

    @property
    def affiliations(self):
        return [
            self.get_text('alinea', dom=affiliation_dom)
            for affiliation_dom in self.findall('affiliation')
        ]

    @property
    def organization(self):
        return self.get_text('nomorg')

    @property
    def role(self):
        find_role = et.XPath('fonction')
        roles = find_role(self._root)
        return {role.get('lang'): role.text for role in roles}

    @property
    def pseudo(self):
        pseudo = self.find('nompers[@typenompers="pseudonyme"]')
        all_person_names = self.findall('nompers')
        if pseudo is not None and len(all_person_names) > 1:
            return DomPersonName(pseudo)
        else:
            return None

    def format_name(self, html=False):
        if not html:
            et.strip_tags(self._root, 'marquage')
        orgname = self.organization
        if orgname:
            return orgname
        result = DomPersonName(self.find('nompers')).format(html=html)
        pseudo = self.pseudo
        if pseudo:
            result += ', alias ' + pseudo.format(html=html)
        return result


class DomRedacteur(DomPerson):
    @property
    def typerc(self):
        return self._root.get('typerc')

    @property
    def themes(self):
        idrefs = self._root.get('idrefs')
        if idrefs:
            return idrefs.split()
        else:
            return []
