import lxml.etree as et

from eruditarticle.objects.dom import DomPerson


def get_dom(fixture_name):
    xml_path = './eruditarticle/tests/fixtures/dom/{}'.format(fixture_name)
    return et.parse(xml_path).getroot()


def test_nomorg_as_text():
    person = DomPerson(get_dom('author_nomorg_formatting.xml'))
    EXPECTED = 'Comité de rédaction de Drogues, santé et société'
    assert person.format_name() == EXPECTED
