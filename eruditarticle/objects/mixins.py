# -*- coding: utf-8 -*-

try:
    from django.utils.translation import pgettext
    from django.utils.translation import gettext as _
except ImportError:
    pgettext = lambda ctx, msg: msg  # noqa
    _ = lambda x: x  # noqa


class PublicationPeriodMixin(object):

    def get_publication_period(self):
        """ Returns the publication period and the year of the publication object. """

        elem = self.find('numero//pub')
        if elem is None:
            return ''
        child_elements = elem.getchildren()
        if not child_elements:
            return ''
        first_element = child_elements.pop(0)
        if first_element.tag == 'annee':
            previous_item_is_year = True
        else:
            previous_item_is_year = False

        publication_period = first_element.text

        for element in child_elements:
            if element.tag == 'periode':
                if previous_item_is_year:
                    publication_period = "{}, {}".format(
                        pgettext("numbering", publication_period),
                        pgettext("numbering", element.text),
                    )
                else:
                    publication_period = "{}–{}".format(
                        pgettext("numbering", publication_period),
                        pgettext("numbering", element.text),
                    )
                previous_item_is_year = False

            if element.tag == 'annee':
                if previous_item_is_year:
                    publication_period = "{}–{}".format(
                        pgettext("numbering", publication_period),
                        pgettext("numbering", element.text)
                    )
                else:
                    publication_period = "{} {}".format(
                        pgettext("numbering", publication_period),
                        pgettext("numbering", element.text)
                    )
                previous_item_is_year = True

        return pgettext("numbering", publication_period)

    publication_period = property(get_publication_period)


class ISBNMixin(object):
    def get_isbn(self):
        """ Returns the ISBN number associated with the article object. """
        isbn = self.get_text('numero//idisbn')
        isbn13 = self.get_text('numero//idisbn13')
        return isbn13 or isbn

    def get_isbn_num(self):
        """ Returns the numeric ISBN number associated with the article object. """
        isbn_num = self.get_text('numero//idisbnnum')
        isbn13_num = self.get_text('numero//idisbnnum13')
        return isbn13_num or isbn_num

    isbn = property(get_isbn)
    isbn_num = property(get_isbn_num)


class ISSNMixin(object):
    def get_issn(self):
        """ Returns the ISSN number associated with the article object. """
        return self.get_text('revue//idissn')

    def get_issn_num(self):
        """ Returns the numeric ISSN number associated with the article object. """
        return self.get_text('revue//idissnnum')

    issn = property(get_issn)
    issn_num = property(get_issn_num)


class CopyrightMixin(object):
    def get_droitsauteur(self):
        """ Return the list of all copyright notices of this object.

        The copyrights are returned as a list of the form:

            [
                {'text': 'My copyright', },
                {'href': 'link-url', 'img': 'img-url', },
            ]

        """
        da_list = []
        da_nodes = self.findall('droitsauteur')

        for da in da_nodes:
            link_node = self.find('liensimple', da)
            if link_node is not None:
                da_list.append(self.parse_simple_link(link_node))
            else:
                da_list.append({'text': ''.join(da.itertext())})

        return da_list

    def get_droitsauteurorg(self):
        """ Return the owner of the first copyright for this object. """
        return self.get_text('droitsauteur/nomorg')

    def _get_copyrights_label(self, root, language, html=False):
        """ Return the copyrights declaration.

        :param root: (object):
            The root XML Element.
        :param language: (str):
            The desired language for the copyrights declaration.
        :param html: (bool, optional): Defaults to False.
            Whether to convert marquage content to HTML.
        :returns: The copyrights declaration as a string. """
        labels = []
        declaration = root.xpath('contributiondeclaration | copyrightdeclaration')
        if len(declaration):
            labels = declaration[0].xpath('label[@lang="{}"]'.format(language)) or \
                     declaration[0].findall('label')
        if len(labels):
            return self.convert_marquage_content_to_html(labels[0]) if html else labels[0].text
        else:
            return ''

    def _get_copyrights_names(self, root, html=False):
        """ Return the list of copyrights holders' names.

        :param root: (object):
            The root XML Element.
        :param html: (bool, optional): Defaults to False.
            Whether to convert marquage content to HTML.
        :returns: The copyrights holders' names as a list of strings. """
        names = []
        for contribution in root.findall('contribution'):
            person = contribution.xpath(' \
                artificialperson/name | \
                physicalperson/personname/firstname | \
                physicalperson/personname/familyname | \
                physicalperson/personname/personnameprefix/name \
            ')
            # Put prefix first if prefix is present.
            if len(person) == 3:
                person = person[-1:] + person[:-1]
            names.append(person)
        formatted_names = []
        for name in names:
            formatted_names.append(' '.join([
                self.convert_marquage_content_to_html(part) if html else part.text
                for part in name
            ]))
        return formatted_names

    def _get_copyrights_year(self, root, html=False):
        """ Return the copyrights year.

        :param root: (object):
            The root XML Element.
        :param html: (bool, optional): Defaults to False.
            Whether to convert marquage content to HTML.
        :returns: The copyrights year as a string. """
        year = root.find('year')
        if year is not None:
            return self.convert_marquage_content_to_html(year) if html else year.text
        else:
            return ''

    def _format_names(self, names):
        """ Format a list of names as a string separated by commas and a 'and' before the last one.

        :param names: (list):
            The list of names to be formatted.
        :returns: The list of names formatted as a string. """
        last_name = names.pop() if len(names) else ''
        if len(names) == 0:
            return last_name
        return '{} {} {}'.format(
            ', '.join(names),
            _('et'),
            last_name,
        )

    def get_copyrights(self, language, formatted=False, html=False):
        """ Return the copyrights notice for this object.

        The copyrights can be returned as a dictionary of the form:

        {
            'label': 'All rights reserved',
            'names': ['Journal Foo', 'Society Bar'],
            'year': '1999',
        }

        Or as a formatted or HTML string of the form:

        'All rights reserved © Journal Foo and Society Bar, 1999'

        :param language: (str):
            The desired language for the copyrights notice.
        :param formatted: (bool, optional): Defaults to False.
            Whether to format the copyrights notice as a string.
        :param html: (bool, optional): Defaults to False.
            Whether to convert marquage content to HTML.
        :returns: The copyrights notice as a dictionary or as a string. """
        root = self.find('copyright')
        if root is None:
            return '' if formatted or html else {}
        label = self._get_copyrights_label(root, language, html)
        names = self._get_copyrights_names(root, html)
        year = self._get_copyrights_year(root, html)
        if html or formatted:
            return '{} © {}, {}'.format(label, self._format_names(names), year)
        else:
            return {'label': label, 'names': names, 'year': year}

    droitsauteur = property(get_droitsauteur)
    droitsauteur_org = property(get_droitsauteurorg)
