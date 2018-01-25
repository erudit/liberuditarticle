import lxml.etree as et

from eruditarticle.objects.dom import DomPerson


def get_dom(fixture_name):
    xml_path = './eruditarticle/tests/fixtures/dom/{}'.format(fixture_name)
    return et.parse(xml_path).getroot()


def test_nomorg_as_text():
    person = DomPerson(get_dom('author_nomorg_formatting.xml'))
    EXPECTED = 'Comité de rédaction de Drogues, santé et société'
    assert person.format_name() == EXPECTED


def test_nomorg_as_html():
    person = DomPerson(get_dom('author_nomorg_formatting.xml'))
    EXPECTED = 'Comit&#233; de r&#233;daction de <em>Drogues, sant&#233; et soci&#233;t&#233;</em>'
    assert person.format_name(html=True) == EXPECTED


def test_nomorg_with_members():
    person = DomPerson(get_dom('author_nomorg_membres.xml'))
    EXPECTED = 'My Org (prenom1 nomfamille1, prenom2 nomfamille2)'
    assert person.format_name() == EXPECTED
