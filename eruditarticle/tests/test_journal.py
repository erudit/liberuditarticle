
import pytest

from eruditarticle.objects import EruditPublication
from eruditarticle.tests.base import BaseTestCase


class TestEruditPublication(BaseTestCase):

    @pytest.fixture(autouse=True)
    def setup(self):
        self.object_type = EruditPublication
        self.objects_path = './eruditarticle/tests/fixtures/publication'
        super().setup()

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
                'paral': {}
            },
            'th2': {
                'name': 'La production au Québec',
                'redacteurchef': [],
                'paral': {}
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
        assert themes['th1']['paral']['en'] == 'Geopolitics'

    def test_redacteurchef(self):
        redacteurchef = self.test_objects['ae1375.xml'].get_redacteurchef()
        assert redacteurchef[0]['firstname'] == 'Olivier'
        assert redacteurchef[0]['lastname'] == 'Donni'
        assert redacteurchef[0]['type'] == 'invite'

        redacteurchef = self.test_objects['images1102374.xml'].get_redacteurchef()  # noqa
        assert redacteurchef[0]['firstname'] == 'Marie-Claude'
        assert redacteurchef[0]['lastname'] == 'Loiselle'
        assert redacteurchef[0]['type'] == 'regulier'

    def test_droitauteur(self):
        assert self.test_objects['images1102374.xml'].get_droitauteur() == "Tous droits réservés © 24 images, 2000"  # noqa
        assert self.test_objects['liberte1035607.xml'].get_droitauteur() == "Tous droits réservés © Collectif Liberté, 1993"  # noqa

    def test_droitauteurorg(self):
        assert self.test_objects['images1102374.xml'].get_droitauteurorg() == "24 images"
        assert self.test_objects['liberte1035607.xml'].get_droitauteurorg() == "Collectif Liberté"

    def test_notegen(self):
        assert self.test_objects['rum01069.xml'].get_notegen_edito() == """POUR NABIHA : Nabiha Jerad, Professeur de socio-linguistique à la Faculté des Lettres de l’Université de Tunis se trouvait dans son île natale, Kerkennah, pour célébrer le Ramadan avec sa famille. Sortie pour prendre l’air avant le dîner, elle fut renversée par une voiture. Le chauffeur - ou plutôt le chauffard - ne s’arrêta pas et s’enfuit. C’était le 11 août 2012. Elle tomba dans un coma dont elle ne se sortira jamais, malgré les soins intensifs et le dévouement du personnel médical, d’abord à Bruxelles, ensuite à Tunis où elle rendit l’âme le 19 octobre 2012. Pour ceux et celles qui l’ont connue, Nabiha avait le coeur sur la main, l’esprit ouvert à “tous les souffles du monde” pour reprendre Aimé Césaire. Elle était d’un grand dévouement envers ses étudiants, très attachée à son pays la Tunisie et fortement engagée dans ce qui fut appelée la Révolution de Jasmin. Son article non achevé, qui devait paraître dans ce volume, se serait ajouté à ses nombreuses autres publications dans le domaine de la socio-linguistique. Cette petite note rappellera la mémoire de celle qui fut non seulement une collègue, mais aussi une amie. Université Laval 3 Juillet 2013 Justin K. Bisanswa"""  # noqa
