import lxml.etree as et
import pytest

from eruditarticle.objects.person import (
    Person, format_authors_mla, format_authors_apa, format_authors_chicago
)


class FakePerson:
    def __init__(self, firstname, lastname, othername='', organization='', pseudo=''):
        self.firstname = firstname
        self.lastname = lastname
        self.othername = othername
        self.organization = organization
        self.pseudo = pseudo

    def strip_markup(self):
        pass


def get_dom(fixture_name):
    xml_path = './eruditarticle/tests/fixtures/dom/{}'.format(fixture_name)
    return et.parse(xml_path).getroot()


def test_nomorg_as_text():
    person = Person(get_dom('author_nomorg_formatting.xml'))
    EXPECTED = 'Comité de rédaction de Drogues, santé et société'
    assert person.format_name() == EXPECTED


def test_nomorg_as_html():
    person = Person(get_dom('author_nomorg_formatting.xml'))
    EXPECTED = 'Comité de rédaction de <em>Drogues, santé et société</em>'
    assert person.format_name(html=True) == EXPECTED


def test_nomorg_with_members():
    person = Person(get_dom('author_nomorg_membres.xml'))
    EXPECTED = 'My Org (prenom1 nomfamille1, prenom2 nomfamille2)'
    assert person.format_name() == EXPECTED


def test_empty_author():
    # Don't crash on author tags that don't have a "nompers"
    person = Person(get_dom('author_empty.xml'))
    EXPECTED = ''
    assert person.format_name() == EXPECTED


def test_author_with_multiple_suffixes():
    person = Person(get_dom('author_with_multiple_suffixes.xml'))
    assert person.format_name() == 'Julien D. Payne, LL.D., Q.C., F.R.S.C.'
    assert person.format_name(suffixes=False) == 'Julien D. Payne'


def test_author_with_empty_suffix():
    person = Person(get_dom('author_with_empty_suffix.xml'))
    assert person.format_name() == 'Pamela A. Foelsch'


COMMON_EDGE_CASES = [
    (
        [], ""
    ),
    (
        [(None, None)], ""
    ),
    (
        [(None, None, None)], ""
    ),
]


@pytest.mark.parametrize('authors,expected', COMMON_EDGE_CASES + [
    (
        [("Firstname", "Lastname")],
        "Lastname, Firstname."
    ),
    (
        [("Firstname", "Lastname", "Othername")],
        "Lastname, Firstname O."
    ),
    (
        [("Firstname", "Lastname", "Other1 Other2")],
        "Lastname, Firstname O. O."
    ),
    (
        [("First1", "Last1"), ("First2", "Last2")],
        "Last1, First1 et First2 Last2."
    ),
    (
        [("First1", "Last1", "Other1"), ("First2", "Last2", "Other2")],
        "Last1, First1 O. et First2 O. Last2."
    ),
    (
        [("First1", "Last1"), ("First2", "Last2"), ("First3", "Last3")],
        "Last1, First1, et al."
    ),
    (
        [("First1", "Last1", "Other1"), ("First2", "Last2", "Other2"), ("First3", "Last3", "Other3")],  # noqa
        "Last1, First1 O., et al."
    ),
    (
        [("Firstname", None)],
        "Firstname."
    ),
    (
        [(None, "Lastname")],
        "Lastname."
    ),
])
def test_format_authors_mla(authors, expected):
    authors = [FakePerson(*args) for args in authors]
    result = format_authors_mla(authors)
    assert result == expected


@pytest.mark.parametrize('authors,expected', COMMON_EDGE_CASES + [
    (
        [("Firstname", "Lastname")],
        "Lastname, F."
    ),
    (
        [("Firstname", "Lastname", "Othername")],
        "Lastname, F. O."
    ),
    (
        [("Firstname", "Lastname", "Other1 Other2")],
        "Lastname, F. O. O."
    ),
    (
        [("First1", "Last1"), ("First2", "Last2")],
        "Last1, F. & Last2, F."
    ),
    (
        [("First1", "Last1", "Other1"), ("First2", "Last2", "Other2")],
        "Last1, F. O. & Last2, F. O."
    ),
    (
        [("First1", "Last1"), ("First2", "Last2"), ("First3", "Last3")],
        "Last1, F., Last2, F. & Last3, F."
    ),
    (
        [("First1", "Last1", "Other1"), ("First2", "Last2", "Other2"), ("First3", "Last3", "Other3")],  # noqa
        "Last1, F. O., Last2, F. O. & Last3, F. O."
    ),
    (
        [("Firstname", None)],
        "Firstname"
    ),
    (
        [(None, "Lastname")],
        "Lastname"
    ),
    (
        [("Composed-Firstname", "Lastname")],
        "Lastname, C.-F."
    ),
])
def test_format_authors_apa(authors, expected):
    authors = [FakePerson(*args) for args in authors]
    result = format_authors_apa(authors)
    assert result == expected


@pytest.mark.parametrize('authors,expected', COMMON_EDGE_CASES + [
    (
        [("Firstname", "Lastname")],
        "Lastname, Firstname"
    ),
    (
        [("Firstname", "Lastname", "Othername")],
        "Lastname, Firstname O."
    ),
    (
        [("Firstname", "Lastname", "Other1 Other2")],
        "Lastname, Firstname O. O."
    ),
    (
        [("First1", "Last1"), ("First2", "Last2")],
        "Last1, First1 et Last2, First2"
    ),
    (
        [("First1", "Last1", "Other1"), ("First2", "Last2", "Other2")],
        "Last1, First1 O. et Last2, First2 O."
    ),
    (
        [("First1", "Last1"), ("First2", "Last2"), ("First3", "Last3")],
        "Last1, First1, Last2, First2 et Last3, First3"
    ),
    (
        [("First1", "Last1", "Other1"), ("First2", "Last2", "Other2"), ("First3", "Last3", "Other3")],  # noqa
        "Last1, First1 O., Last2, First2 O. et Last3, First3 O."
    ),
    (
        [("Firstname", None)],
        "Firstname"
    ),
    (
        [(None, "Lastname")],
        "Lastname"
    ),
])
def test_format_authors_chicago(authors, expected):
    authors = [FakePerson(*args) for args in authors]
    result = format_authors_chicago(authors)
    assert result == expected
