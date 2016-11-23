# -*- coding: utf-8 -*-


class PublicationPeriodMixin(object):

    def get_publication_period(self):
        """ Returns the publication period and the year of the publication object. """

        child_elements = self.find('numero//pub').getchildren()
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
                        publication_period,
                        element.text,
                    )
                else:
                    publication_period = "{}–{}".format(
                        publication_period,
                        element.text,
                    )
                previous_item_is_year = False

            if element.tag == 'annee':
                if previous_item_is_year:
                    publication_period = "{}–{}".format(
                        publication_period,
                        element.text
                    )
                else:
                    publication_period = "{} {}".format(
                        publication_period,
                        element.text
                    )
                previous_item_is_year = True

        return publication_period

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
            if link_node:
                da_list.append(self.parse_simple_link(link_node))
            else:
                da_list.append({'text': ''.join(da.itertext())})

        return da_list

    def get_droitsauteurorg(self):
        """ Return the owner of the first copyright for this object. """
        return self.get_text('droitsauteur/nomorg')

    droitsauteur = property(get_droitsauteur)
    droitsauteur_org = property(get_droitsauteurorg)
