import pytest
from eruditarticle.objects import EruditPublication

try:
    from django.utils import translation  # noqa
except ImportError:
    pytestmark = pytest.mark.skip(reason="Django is not installed")

from .decorators import with_fixtures, with_value, with_locale


@with_locale("en")
@with_fixtures(
    "./eruditarticle/tests/fixtures/publication/volume_numbering", EruditPublication
)
class TestPublicationVolumeNumberingEnglish(object):
    @with_value("cd02305.xml", "get_volume_numbering", formatted=True)
    def test_can_format_volume_and_number_in_en(self, value):
        assert value == "Volume 56, Number 3-4, September–December 2015"

    @with_value("annuaire3703.xml", "get_volume_numbering", formatted=True)
    def test_can_format_volume_numbering_horsserie_year_in_en(self, value):
        assert value == "Special Issue, 2001"

    @with_value("haf2442.xml", "get_volume_numbering", formatted=True)
    def test_can_format_volume_numbering_in_case_of_index_in_en(self, value):
        assert value == "Index, 1997"

    @with_value("sequences1128840.xml", "get_volume_numbering", formatted=True)
    def test_can_format_volume_numbering_no_volume_multiple_months_in_en(self, value):
        assert value == "Number 211, January–February 2001"

    @with_value("sequences1081634.xml", "get_volume_numbering", formatted=True)
    def test_can_format_volume_numbering_in_case_of_index_with_number_in_en(
        self, value
    ):
        assert value == "Number 125, Index, 1986"

    @with_value("inter1068986.xml", "get_volume_numbering", formatted=True)
    def test_can_format_volume_numbering_in_case_of_supplement_in_en(self, value):
        assert value == "Number 110, Supplement, Winter 2012"

    @with_value("ehr1825418.xml", "get_volume_numbering", formatted=True)
    def test_can_format_volume_publication_period_in_en(self, value):
        assert value == "Volume 73, 2007"

    @with_value("crs1517600.xml", "get_volume_numbering", formatted=True)
    def test_can_format_volume_numbering_in_case_of_horsserie_in_en(self, value):
        assert value == "Special Issue, 2003"

    @with_value("va1503694.xml", "get_volume_numbering", formatted=True)
    def test_can_format_volume_number_numbertype_in_en(self, value):
        assert value == "Volume 52, Number 214, Supplement, Spring 2009"

    @with_value("as2866.xml", "get_volume_numbering", formatted=True)
    def test_can_format_volume_numbering_horsserie_no_number_in_en(self, value):
        assert value == "Volume 32, Special Issue, 2008"
