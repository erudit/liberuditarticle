
import pytest

from eruditarticle.base import Title
from eruditarticle.objects import EruditPublication
from eruditarticle.tests.base import BaseTestCase


class TestEruditPublication(BaseTestCase):

    @pytest.fixture(autouse=True)
    def setup(self):
        self.object_type = EruditPublication
        self.objects_path = './eruditarticle/tests/fixtures/publication'
        super().setup()

    def test_number(self):
        assert self.test_objects["ae1375.xml"].get_number() == '1-2'
        assert self.test_objects["crs1517600.xml"].get_number() == ''
        assert self.test_objects["esse02315.xml"].get_number() == '86'

    def test_can_return_its_title(self):
        assert self.test_objects["ae1375.xml"].get_titles(strip_markup=True) == {
            'main': Title(title="L'Actualité économique", subtitle=None, lang="fr"),
            'paral': [],
            'equivalent': [],
        }

        assert self.test_objects["crs1517600.xml"].get_titles(strip_markup=True) == {
            'main': Title(title="Cahiers de recherche sociologique", subtitle=None, lang="fr"),
            'paral': [],
            'equivalent': [],
        }

        assert self.test_objects["mje02648.xml"].get_titles(strip_markup=True) == {
            'main': Title(title="McGill Journal of Education", subtitle=None, lang="en"),
            'paral': [Title(title="Revue des sciences de l'éducation de McGill", subtitle=None, lang="fr")],  # noqa
            'equivalent': [],
        }

    def test_publicationtype(self):
        assert self.test_objects["haf2442.xml"].get_publication_type() == 'index'
        assert self.test_objects["inter1068986.xml"].get_publication_type() == 'supp'
        assert self.test_objects["crs1517600.xml"].get_publication_type() == 'hs'

    def test_themes(self):
        themes = self.test_objects["images1080663.xml"].get_themes()
        assert themes == {
            'th1': {
                'name': 'David Cronenberg',
                'redacteurchef': [],
                'paral': {},
                'subname': None,
                'html_name': b'David Cronenberg',
                'html_subname': None,
            },
            'th2': {
                'name': 'La production au Québec',
                'redacteurchef': [],
                'paral': {},
                'subname': 'Cinq cinéastes sur le divan',
                'html_name': b'La production au Qu&#233;bec',
                'html_subname': b'Cinq cin&#233;astes sur le divan',
            },
        }

    def test_multiple_themes_multiple_redacteur(self):
        themes = self.test_objects['smq1826.xml'].get_themes()
        assert len(themes.keys()) == 2
        assert len(themes["th1"]["redacteurchef"]) == 1
        assert len(themes["th2"]["redacteurchef"]) == 3
        assert themes["th1"]["redacteurchef"][0]['firstname'] == "Alain"
        assert themes["th1"]["redacteurchef"][0]['lastname'] == "Lesage"

    def test_theme_paral(self):
        themes = self.test_objects['esse02315.xml'].get_themes()
        assert len(themes.keys()) == 1
        assert themes['th1']['name'] == 'Géopolitique'
        assert themes['th1']['paral']['en'] == {
            'name': 'Geopolitics', 'subname': None, 'html_name': b'Geopolitics',
            'html_subname': None, }

    def test_sstheme(self):
        themes = self.test_objects['images1080663.xml'].get_themes()
        assert len(themes.keys()) == 2
        assert themes['th2'] == {
            'name': 'La production au Québec',
            'paral': {},
            'redacteurchef': [],
            'subname': 'Cinq cinéastes sur le divan',
            'html_name': b'La production au Qu&#233;bec',
            'html_subname': b'Cinq cin&#233;astes sur le divan',
        }

    def test_redacteurchef(self):
        redacteurchef = self.test_objects['ae1375.xml'].get_redacteurchef()
        assert redacteurchef[0]['firstname'] == 'Olivier'
        assert redacteurchef[0]['lastname'] == 'Donni'
        assert redacteurchef[0]['type'] == 'invite'

        redacteurchef = self.test_objects['images1102374.xml'].get_redacteurchef()  # noqa
        assert redacteurchef[0]['firstname'] == 'Marie-Claude'
        assert redacteurchef[0]['lastname'] == 'Loiselle'
        assert redacteurchef[0]['type'] == 'regulier'

    def test_droitsauteur(self):
        assert self.test_objects['images1102374.xml'].get_droitsauteur() == [{'text': "Tous droits réservés © 24 images, 2000"}]  # noqa
        assert self.test_objects['liberte1035607.xml'].get_droitsauteur() == [{'text': "Tous droits réservés © Collectif Liberté, 1993"}]  # noqa
        assert self.test_objects['ritpu0326.xml'].get_droitsauteur()[0] == {'text': 'Tous droits réservés © CRÉPUQ,'}  # noqa
        assert self.test_objects['ritpu0326.xml'].get_droitsauteur()[1] == {
            'href': 'http://creativecommons.org/licenses/by-nc-sa/3.0/deed.fr_CA',
            'img': 'http://i.creativecommons.org/l/by-nc-sa/3.0/88x31.png',
        }

    def test_droitsauteurorg(self):
        assert self.test_objects['images1102374.xml'].get_droitsauteurorg() == "24 images"
        assert self.test_objects['liberte1035607.xml'].get_droitsauteurorg() == "Collectif Liberté"

    def test_notegen(self):
        assert self.test_objects['rum01069.xml'].get_notegen_edito() == """POUR NABIHA : Nabiha Jerad, Professeur de socio-linguistique à la Faculté des Lettres de l’Université de Tunis se trouvait dans son île natale, Kerkennah, pour célébrer le Ramadan avec sa famille. Sortie pour prendre l’air avant le dîner, elle fut renversée par une voiture. Le chauffeur - ou plutôt le chauffard - ne s’arrêta pas et s’enfuit. C’était le 11 août 2012. Elle tomba dans un coma dont elle ne se sortira jamais, malgré les soins intensifs et le dévouement du personnel médical, d’abord à Bruxelles, ensuite à Tunis où elle rendit l’âme le 19 octobre 2012. Pour ceux et celles qui l’ont connue, Nabiha avait le coeur sur la main, l’esprit ouvert à “tous les souffles du monde” pour reprendre Aimé Césaire. Elle était d’un grand dévouement envers ses étudiants, très attachée à son pays la Tunisie et fortement engagée dans ce qui fut appelée la Révolution de Jasmin. Son article non achevé, qui devait paraître dans ce volume, se serait ajouté à ses nombreuses autres publications dans le domaine de la socio-linguistique. Cette petite note rappellera la mémoire de celle qui fut non seulement une collègue, mais aussi une amie. Université Laval 3 Juillet 2013 Justin K. Bisanswa"""  # noqa

    def test_issn(self):
        assert self.test_objects['ae1375.xml'].issn == '0001-771X'

    def test_issn_num(self):
        assert self.test_objects['ae1375.xml'].issn_num == '1710-3991'

    def test_isbn(self):
        assert self.test_objects['crs1517600.xml'].isbn == '2-89578-037-4'
        assert self.test_objects['inter02349.xml'].isbn == '978-2-924298-19-0'
        assert self.test_objects['esse02315.xml'].isbn is None

    def test_isbn_num(self):
        assert self.test_objects['esse02315.xml'].isbn_num == '978-2-924345-09-2'
        assert self.test_objects['inter02349.xml'].isbn_num == '978-2-924298-20-6'
        assert self.test_objects['crs1517600.xml'].isbn_num is None

    def test_note_edito(self):
        assert self.test_objects['rum01069.xml'].note_edito.startswith('POUR NABIHA')
        assert self.test_objects['rum01069.xml'].note_edito.endswith('Bisanswa')

    def test_guest_editors(self):
        assert self.test_objects['ae1375.xml'].guest_editors == [{
            'affiliations': [],
            'othername': None,
            'firstname': 'Olivier',
            'email': None,
            'lastname': 'Donni',
            'organization': None,
            'role': {},
            'suffix': None,
        }]

    def test_directors(self):
        assert self.test_objects['ae1375.xml'].directors == [{
            'affiliations': [],
            'othername': None,
            'firstname': 'Patrick',
            'email': None,
            'lastname': 'González',
            'organization': None,
            'role': {},
            'suffix': None,
        }]

        assert self.test_objects['haf2442.xml'].directors == [{
            'affiliations': [],
            'othername': None,
            'firstname': 'Fernande',
            'email': None,
            'lastname': 'Roy',
            'organization': None,
            'role': {'fr': 'Directrice'},
            'suffix': None,
        }]

        assert 'role_en' not in self.test_objects['haf2442.xml'].directors

    def test_editors(self):
        assert self.test_objects['images1080663.xml'].editors == [{
            'affiliations': [],
            'othername': None,
            'firstname': 'Isabelle',
            'lastname': 'Richer',
            'email': None,
            'organization': None,
            'role': {'fr': 'Rédactrice adjointe'},
            'suffix': None,
        }]

    def test_can_find_roles_in_all_languages(self):
        directors = self.test_objects['haf2442-alt.xml'].directors
        assert len(directors) == 1
        director = directors[0]
        assert 'role_fr' not in director and 'role_en' not in director
        assert director['role'] == {'es': 'Directrice'}

    def test_roles_are_associated_with_the_proper_person(self):
        """ Test that an editor only has his own roles """
        editors = self.test_objects['mje02648.xml'].editors
        editor = editors[0]

        assert editor['lastname'] == 'Strong-Wilson'
        assert 'fr' not in editor['role']
        assert editor['role']['en'] == "Editor-in-Chief / Rédactrice-en-chef"
