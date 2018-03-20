from collections import namedtuple

import lxml.etree as et
import pytest

from eruditarticle.objects.person import (
    Person, format_authors_mla, format_authors_apa, format_authors_chicago
)


FakePerson = namedtuple('Person', 'firstname lastname othername')


def get_dom(fixture_name):
    xml_path = './eruditarticle/tests/fixtures/dom/{}'.format(fixture_name)
    return et.parse(xml_path).getroot()


def test_nomorg_as_text():
    person = Person(get_dom('author_nomorg_formatting.xml'))
    EXPECTED = 'Comité de rédaction de Drogues, santé et société'
    assert person.format_name() == EXPECTED


def test_nomorg_as_html():
    person = Person(get_dom('author_nomorg_formatting.xml'))
    EXPECTED = 'Comit&#233; de r&#233;daction de <em>Drogues, sant&#233; et soci&#233;t&#233;</em>'
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


@pytest.mark.parametrize('authors,expected', [
    (
        [],
        ""
    ),
    (
        [("Firstname", "Lastname", "")],
        "Lastname, Firstname."
    ),
    (
        [("Firstname", "Lastname", "Othername")],
        "Othername."
    ),
    (
        [("First1", "Last1", ""), ("First2", "Last2", "")],
        "Last1, First1 et First2 Last2"
    ),
    (
        [("First1", "Last1", "Other1"), ("First2", "Last2", "Other2")],
        "Other1 et Other2"
    ),
])
def test_format_authors_mla(authors, expected):
    authors = [FakePerson(*args) for args in authors]
    result = format_authors_mla(authors)
    assert result == expected


@pytest.mark.parametrize('authors,expected', [
    (
        [],
        ""
    ),
    (
        [("Firstname", "Lastname", "")],
        "Lastname, F."
    ),
    (
        [("Firstname", "Lastname", "Othername")],
        "Othername"
    ),
    (
        [("First1", "Last1", ""), ("First2", "Last2", "")],
        "Last1, F. & Last2, F."
    ),
    (
        [("First1", "Last1", "Other1"), ("First2", "Last2", "Other2")],
        "Other1 & Other2"
    ),
    (
        [("First1", "Last1", ""), ("First2", "Last2", ""), ("First3", "Last3", "")],
        "Last1, F., Last2, F. & Last3, F."
    ),
])
def test_format_authors_apa(authors, expected):
    authors = [FakePerson(*args) for args in authors]
    result = format_authors_apa(authors)
    assert result == expected


@pytest.mark.parametrize('authors,expected', [
    (
        [],
        ""
    ),
    (
        [("Firstname", "Lastname", "")],
        "Lastname, Firstname"
    ),
    (
        [("Firstname", "Lastname", "Othername")],
        "Othername"
    ),
    (
        [("First1", "Last1", ""), ("First2", "Last2", "")],
        "Last1, First1 et Last2, First2"
    ),
    (
        [("First1", "Last1", "Other1"), ("First2", "Last2", "Other2")],
        "Other1 et Other2"
    ),
    (
        [("First1", "Last1", ""), ("First2", "Last2", ""), ("First3", "Last3", "")],
        "Last1, First1, Last2, First2 et Last3, First3"
    ),
])
def test_format_authors_chicago(authors, expected):
    authors = [FakePerson(*args) for args in authors]
    result = format_authors_chicago(authors)
    assert result == expected
