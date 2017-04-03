
import pytest

from eruditarticle.objects import EruditJournal
from eruditarticle.tests.base import BaseTestCase


class TestEruditPublication(BaseTestCase):

    @pytest.fixture(autouse=True)
    def setup(self):
        self.object_type = EruditJournal
        self.objects_path = './eruditarticle/tests/fixtures/journal'
        super().setup()

    def test_can_return_first_publication_year(self):
        assert self.test_objects['mi115.xml'].get_first_publication_year() == '2009'

    def test_can_return_last_publication_year(self):
        assert self.test_objects['mi115.xml'].get_last_publication_year() == '2015'

    def test_can_return_publication_period(self):
        assert self.test_objects['mi115.xml'].get_publication_period() == '2009 - 2015'

    def test_can_return_publication_years(self):
        assert self.test_objects['mi115.xml'].get_publication_years() == [
            '2009', '2010', '2011', '2012', '2013', '2014', '2015'
        ]

    def test_can_return_journal_name(self):
        assert self.test_objects['mi115.xml'].get_title() == "Management international / International Management / Gestiòn Internacional"  # noqa
