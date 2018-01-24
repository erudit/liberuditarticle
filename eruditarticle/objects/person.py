import lxml.etree as et

from .base import DomObject


class DomPerson(DomObject):
    # NOTE: This is one of the slowest parts of liberuditarticle.
    #
    # Searching for slow tests and profiling the code led to discover that this
    # function was a bottleneck. When asking for a "html" person, a XSL transfo
    # is performed for every tag. An optimization would be to perform *one*
    # XSL transformation for the whole sub tree.

    def __init__(self, root, html=False):
        super().__init__(root)
        self._html_output = html
        et.strip_tags(self._root, 'marquage')

    def _getval(self, tagname, dom=None):
        if self._html_output:
            return self.get_html(tagname, dom)
        else:
            return self.get_text(tagname, dom)

    @property
    def firstname(self):
        return self._getval('prenom')

    @property
    def lastname(self):
        return self._getval('nomfamille')

    @property
    def othername(self):
        return self._getval('autreprenom')

    @property
    def suffix(self):
        return self._getval('suffixe')

    @property
    def email(self):
        return self._getval('courriel/liensimple')

    @property
    def affiliations(self):
        return [
            self._getval('alinea', dom=affiliation_dom)
            for affiliation_dom in self.findall('affiliation')
        ]

    @property
    def organization(self):
        return self._getval('nomorg')

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
            return DomPerson(pseudo, html=self._html_output)
        else:
            return None

    def format_name(self, html=False):
        # The line below is a bit of a hack but is necessary to keep the exact same semantic as
        # before the refactoring. With usage, we can explore the feasability of getting rid of
        # the `html` flag of this function and always use `self`.
        person = self if html == self._html_output else DomPerson(self._root, html=html)
        keys_order = ['firstname', 'othername', 'lastname', 'suffix']
        ordered_vals = [getattr(person, key) for key in keys_order]
        result = ' '.join(v for v in ordered_vals if v)
        pseudo = person.pseudo
        if pseudo:
            result += ', alias ' + pseudo.format_name(html=html)

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
