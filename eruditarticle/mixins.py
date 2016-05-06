# -*- coding: utf-8 -*-


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
