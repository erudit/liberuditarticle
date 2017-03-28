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

    def test_can_return_titles_subtitles(self):
        from eruditarticle.base import Title

        assert self.test_objects['1005860ar.xml'].get_titles() == {
            'main': Title(title="Esth&#233;tique et s&#233;miotique", subtitle="Pr&#233;sentation", lang="fr"),  # noqa
            "paral": [
                Title(title="Aesthetics and Semiotics", lang="en", subtitle="Presentation")  # noqa
            ],
            "equivalent": [],
            'reviewed_works': []
        }

        assert self.test_objects['044308ar.xml'].get_titles() == {
            'main': Title(title=None, subtitle=None, lang="fr"),
            'paral': [],
            'equivalent': [],
            'reviewed_works': [
                    '<em>Sociologie des relations professionnelles</em>, Par Michel Lallement, Nouvelle &#233;dition, Paris&#160;: La D&#233;couverte, collection Rep&#232;res, 2008, 121&#160;p., ISBN 978-2-7071-5446-0.',  # noqa
                    '<em>Sociologie du travail&#160;: les relations professionnelles</em>, Par Antoine Bevort et Annette Jobert, Paris&#160;: Armand Collin, collection U, 2008, 268&#160;p., ISBN 978-2-200-34571-6.'  # noqa
            ]
        }

        assert self.test_objects['1004725ar.xml'].get_titles() == {
            'main': Title(title="Introduction: Food, Language, and Identity", subtitle=None, lang="en"),  # noqa
            'paral': [],
            'equivalent': [Title(title="Cuisine, langue et identit&#233;", subtitle=None, lang="fr")],  # noqa
            'reviewed_works': [],
        }

        assert self.test_objects['1003507ar.xml'].get_titles() == {
            'main': Title(title="Reconceptualizing Translation &#8211; Some Chinese Endeavours", subtitle=None, lang="en"),  # noqa
            'paral': [],
            'equivalent': [],
            'reviewed_works': [],
        }

        assert self.test_objects['1006389ar.xml'].get_titles() == {
            'main': Title(title=None, subtitle=None, lang="fr"),  # noqa
            'paral': [],
            'equivalent': [],
            'reviewed_works': [
                'C<span class="petitecap">oulombe</span> Maxime, 2010, <em>Le monde sans fin des jeux vid&#233;o</em>. Paris, Presses universitaires de France, coll. La nature humaine, 160 p., bibliogr.'  # noqa
            ],
        }

    def test_can_return_formatted_titles(self):
        assert self.test_objects['1005860ar.xml'].get_formatted_html_title() == "Esth&#233;tique et s&#233;miotique :\xa0Pr&#233;sentation / Aesthetics and Semiotics : Presentation"  # noqa

        assert self.test_objects['044308ar.xml'].get_formatted_html_title() == '<em>Sociologie des relations professionnelles</em>, Par Michel Lallement, Nouvelle &#233;dition, Paris&#160;: La D&#233;couverte, collection Rep&#232;res, 2008, 121&#160;p., ISBN 978-2-7071-5446-0. / <em>Sociologie du travail&#160;: les relations professionnelles</em>, Par Antoine Bevort et Annette Jobert, Paris&#160;: Armand Collin, collection U, 2008, 268&#160;p., ISBN 978-2-200-34571-6.'  # noqa

    def test_can_return_journal_titles(self):
        from eruditarticle.base import Title

        assert self.test_objects['1006389ar.xml'].get_journal_titles() == {
            "main": Title(title="Anthropologie et Soci&#233;t&#233;s", subtitle=None, lang="fr"),
            "paral": [],
            "equivalent": [],
        }

        assert self.test_objects['1005860ar.xml'].get_journal_titles() == {
            "main": Title(title="Recherches s&#233;miotiques", subtitle=None, lang="fr"),
            "paral": [Title(title="Semiotic Inquiry", subtitle=None, lang="en")],
            "equivalent": [],
        }

        assert self.test_objects['044308ar.xml'].get_journal_titles() == {
            "main": Title(title="Relations industrielles", subtitle=None, lang="fr"),
            "paral": [],
            "equivalent": [Title(title="Industrial Relations", subtitle=None, lang="en")],
        }

    def test_can_return_its_formatted_journal_title(self):
        assert self.test_objects['1005860ar.xml'].get_formatted_journal_title() == "Recherches s&#233;miotiques / Semiotic Inquiry"  # noqa
        assert self.test_objects['044308ar.xml'].get_formatted_journal_title() == "Relations industrielles"  # noqa

    def test_can_return_languages(self):
        assert self.test_objects['1005860ar.xml'].get_languages() == ['fr', 'en']

    def test_can_return_references(self):
        references = self.test_objects['009255ar.xml'].get_references(strip_markup=True)
        assert references[0] == {'title': "Akenside, Mark. Poems. London: J. Dodsley, 1772.", 'doi': None}  # noqa
        assert len(references) == 53

        references = self.test_objects['1003507ar.xml'].get_references(strip_markup=True)
        assert references[3] == {'title': "Cheung, Martha P. Y. (2005): ‘To translate’ means ‘to exchange’? A new interpretation of the earliest Chinese attempts to define translation (‘fanyi’). Target. 17(1):27-48.", 'doi': '10.1075/target.17.1.03che'}  # noqa

    def test_can_return_references_with_markup(self):
        references = self.test_objects['009255ar.xml'].get_references()
        assert references[0] == {'title': "Akenside, Mark.  <em>Poems</em>.  London: J. Dodsley, 1772.", 'doi': None}  # noqa
        assert len(references) == 53


class TestArticleSavantMinimal(BaseTestCase):

    @pytest.fixture(autouse=True)
    def setup(self):
        self.object_type = EruditArticle
        self.objects_path = './eruditarticle/tests/fixtures/article/savant/minimal'
        super().setup()

    def test_can_return_titles_and_subtitles(self):
        from eruditarticle.base import Title
        assert self.test_objects['602354ar.xml'].get_titles(strip_markup=True) == {
            'main': Title(title='Immigration, langues et performance économique : le Québec et l’Ontario entre 1970 et 1995', lang="fr", subtitle=None),  # noqa
            'equivalent': [
                Title(title='Immigration, Languages and Economic Performance: Quebec and Ontario between 1970 and 1995', lang='en', subtitle=None)  # noqa
            ],
            'paral': [],
            'reviewed_works': [],
        }

    def test_can_return_titles_with_malformed_grtitre(self):
        assert self.test_objects['001296ar.xml'].get_formatted_title() is not None


class TestArticleCulturelMinimal(BaseTestCase):

    @pytest.fixture(autouse=True)
    def setup(self):
        self.object_type = EruditArticle
        self.objects_path = './eruditarticle/tests/fixtures/article/culturel/minimal'
        super().setup()

    def test_all_instances(self):
        for object_name, article in self.test_objects.items():
            assert isinstance(article, EruditArticle)

    def test_can_return_its_title(self):
        from eruditarticle.base import Title
        assert self.test_objects['49222ac.xml'].get_titles(strip_markup=True) == {
            'main': Title(
                title='Love and death on long island',
                subtitle='Premier délice',
                lang='fr',
            ),
            'paral': [],
            'equivalent': [],
            'reviewed_works': ["Love and Death on Long Island (Rendez-vous à Long Island), Grande-Bretagne / Canada, 1997, 93 minutes"]  # noqa
        }

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

    def test_can_extract_reviewed_works(self):
        assert self.test_objects['49222ac.xml'].get_reviewed_works(strip_markup=True) == ["Love and Death on Long Island (Rendez-vous à Long Island), Grande-Bretagne / Canada, 1997, 93 minutes"]  # noqa
