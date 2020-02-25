# -*- coding: utf-8 -*-

from .base import EruditBaseObject


class EruditJournal(EruditBaseObject):

    def get_title(self):
        """ :returns: the title of the journal """
        return self.find('setName').text

    def get_first_publication_year(self):
        """ :returns: the first publication year of the journal. """
        pubyears = self.get_publication_years()
        return pubyears[0] if pubyears else None

    def get_last_publication_year(self):
        """ :returns: the last publication year of the journal. """
        pubyears = self.get_publication_years()
        return pubyears[-1] if pubyears else None

    def has_published_issues(self):
        """ :returns: True if the journal has any published issues, False otherwise. """
        return bool(len(self.findall('numero')))

    def get_published_issues_pids(self):
        """ :returns: the list of published issues pids """
        return [
            numero.get('pid') for numero in
            self.findall('numero')
        ]

    def get_last_published_issue_pid(self):
        """ :returns: the last issue published by this journal. """
        issue = self.find('numero')
        if issue is not None:
            return issue.get('pid')
        return None

    def get_publication_period(self):
        """ :returns: the publication period of the journal object. """
        pubyears = self.get_publication_years()
        years_count = len(pubyears)
        if years_count > 1:
            return '{} - {}'.format(pubyears[0], pubyears[-1])
        elif years_count:
            return pubyears[0]

    def get_publication_years(self):
        """ :returns: the publication period of the journal object. """
        pubyears = []
        for tree_year in self.findall('annee'):
            pubyears.append(tree_year.get('valeur'))
        pubyears = sorted(pubyears)
        return pubyears

    def get_notes(self, html=False, journal_pid=None):
        """ Return the journal's notes.

        The notes are returned as a dictionary of the form:

        {
            'fr': ['Note 1', 'Note 2'],
            'en': ['Note 1', 'Note 2'],
        }

        :param html: (bool, optional): Defaults to False.
            Whether to convert marquage content to HTML.
        :param journal_pid: (str, optional): Only return the notes from the given journal pid.
            For journals with a previous or next journal, we may have notes that only concern one
            of them and we may want to filter those that do not concern us.
        :returns: The journal's notes as a dictionary. """
        notes = {}
        for note in self.findall('note'):
            if journal_pid is not None and journal_pid != note.get('pid'):
                continue
            lang = note.get('langue')
            if lang is None or note.text is None:
                continue
            if lang not in notes:
                notes.update({lang: []})
            notes[lang].append(
                self.convert_marquage_content_to_html(note) if html else note.text
            )
        return notes

    first_publication_year = property(get_first_publication_year)
    last_publication_year = property(get_last_publication_year)
    publication_period = property(get_publication_period)
