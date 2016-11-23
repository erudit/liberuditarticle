import pytest

from eruditarticle.objects import EruditArticle
from eruditarticle.tests.base import BaseTestCase


class TestArticleSavantComplet(BaseTestCase):

    @pytest.fixture(autouse=True)
    def setup(self):
        self.object_type = EruditArticle
        self.objects_path = './eruditarticle/tests/fixtures/article/savant/complet'
        super().setup()

    def test_all_instances(self):
        for object_name, article in self.test_objects.items():
            assert isinstance(article, EruditArticle)

    def test_issn(self):
        assert self.test_objects['1001948ar.xml'].get_issn() == '0001-771X'

    def test_issn_num(self):
        assert self.test_objects['1001948ar.xml'].get_issn_num() == '1710-3991'

    def test_isbn(self):
        assert self.test_objects['1001948ar.xml'].get_isbn() is None

    def test_isbn_num(self):
        assert self.test_objects['1001948ar.xml'].get_isbn_num() is None

    def test_html_title(self):
        assert self.test_objects['1001948ar.xml'].get_html_title() == b'La pr&#233;cision des analystes financiers en Europe&#160;: l&#8217;effet pays et l&#8217;effet secteur revisit&#233;s'  # noqa
        assert self.test_objects['1001948ar_alt.xml'].get_html_title() == b'La pr&#233;cision des analystes financiers en Europe&#160;: l&#8217;effet pays et l&#8217;effet secteur <strong>test</strong> test 2  revisit&#233;s'   # noqa

    def test_publication_period(self):
        assert self.test_objects['1001948ar.xml'].get_publication_period() == 'Juin 2010'
        assert self.test_objects['009255ar.xml'].get_publication_period() ==\
            'November 2003, February 2004'
        assert self.test_objects['1005860ar.xml'].get_publication_period() == "2008–2009"


class TestArticleSavantMinimal(BaseTestCase):

    @pytest.fixture(autouse=True)
    def setup(self):
        self.object_type = EruditArticle
        self.objects_path = './eruditarticle/tests/fixtures/article/savant/minimal'
        super().setup()

    def test_can_return_titles_and_title_paral(self):

        assert self.test_objects['602354ar.xml'].get_titles() == {
            'title': 'Immigration, langues et performance économique : le Québec et l’Ontario entre 1970 et 1995',  # noqa

            'paral': {
                'en': 'Immigration, Languages and Economic Performance: Quebec and Ontario between 1970 and 1995'  # noqa
            }
        }


class TestArticleCulturelMinimal(BaseTestCase):

    @pytest.fixture(autouse=True)
    def setup(self):
        self.object_type = EruditArticle
        self.objects_path = './eruditarticle/tests/fixtures/article/culturel/minimal'
        super().setup()

    def test_all_instances(self):
        for object_name, article in self.test_objects.items():
            assert isinstance(article, EruditArticle)

    def test_issn(self):
        assert self.test_objects['34598ac.xml'].get_issn() == '0835-7641'

    def test_issn_num(self):
        assert self.test_objects['34598ac.xml'].get_issn_num() == '1923-3205'

    def test_isbn(self):
        assert self.test_objects['34598ac.xml'].get_isbn() == '2-922607-82-8'

    def test_isbn_num(self):
        assert self.test_objects['34598ac.xml'].get_isbn_num() is None

    def test_publication_period(self):
        assert self.test_objects['34598ac.xml'].get_publication_period() == 'Juin–Juillet–Août 2008'
        assert self.test_objects['49222ac.xml'].get_publication_period() == 'Mai–Juin 1998'
        assert self.test_objects['65943ac.xml'].get_publication_period() ==\
            'Février–Mars–Avril–Mai 2012'

    def test_can_extract_bibliographic_reference(self):
        assert self.test_objects['49222ac.xml'].get_bibliographic_reference() == "Love and Death on Long Island (Rendez-vous à Long Island), Grande-Bretagne / Canada, 1997, 93 minutes"  # noqa
