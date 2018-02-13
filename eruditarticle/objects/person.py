import lxml.etree as et

from .dom import DomObject


class PersonName(DomObject):
    def format(self, html=False):
        get = self.get_html if html else self.get_text
        keys_order = ['prenom', 'autreprenom', 'nomfamille', 'suffixe']
        ordered_vals = [get(key) for key in keys_order]
        return ' '.join(v for v in ordered_vals if v)


class Person(DomObject):
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
            return PersonName(pseudo)
        else:
            return None

    def format_name(self, html=False):
        if html:
            get = self.get_html
        else:
            get = self.get_text
            et.strip_tags(self._root, 'marquage')
        if self.find('nomorg') is not None:
            # Our "person" is in fact an organization. Special rules apply.
            result = get('nomorg')
            member_elems = self.findall('membre')
            if member_elems:
                members = (PersonName(elem.find('nompers')) for elem in member_elems)
                formatted_members = ', '.join(m.format(html=html) for m in members)
                result = '{} ({})'.format(result, formatted_members)
            return result
        result = PersonName(self.find('nompers')).format(html=html)
        pseudo = self.pseudo
        if pseudo:
            result += ', alias ' + pseudo.format(html=html)
        return result


class Redacteur(Person):
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
