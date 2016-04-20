
import pytest

from eruditarticle.objects import EruditPublication
from eruditarticle.tests.base import BaseTestCase


class TestEruditPublication(BaseTestCase):

    @pytest.fixture(autouse=True)
    def setup(self):
        self.object_type = EruditPublication
        self.objects_path = './eruditarticle/tests/fixtures/publication'
        super().setup()

    def test_droitauteur(self):
        assert self.test_objects['images1102374.xml'].get_droitauteur() == "Tous droits réservés © 24 images, 2000"  # noqa
        assert self.test_objects['liberte1035607.xml'].get_droitauteur() == "Tous droits réservés © Collectif Liberté, 1993"  # noqa

    def test_droitauteurorg(self):
        assert self.test_objects['images1102374.xml'].get_droitauteurorg() == "24 images"
        assert self.test_objects['liberte1035607.xml'].get_droitauteurorg() == "Collectif Liberté"

    def test_notegen(self):
        assert self.test_objects['rum01069.xml'].get_notegen_edito() == """POUR NABIHA : Nabiha Jerad, Professeur de socio-linguistique à la Faculté des Lettres de l’Université de Tunis se trouvait dans son île natale, Kerkennah, pour célébrer le Ramadan avec sa famille. Sortie pour prendre l’air avant le dîner, elle fut renversée par une voiture. Le chauffeur - ou plutôt le chauffard - ne s’arrêta pas et s’enfuit. C’était le 11 août 2012. Elle tomba dans un coma dont elle ne se sortira jamais, malgré les soins intensifs et le dévouement du personnel médical, d’abord à Bruxelles, ensuite à Tunis où elle rendit l’âme le 19 octobre 2012. Pour ceux et celles qui l’ont connue, Nabiha avait le coeur sur la main, l’esprit ouvert à “tous les souffles du monde” pour reprendre Aimé Césaire. Elle était d’un grand dévouement envers ses étudiants, très attachée à son pays la Tunisie et fortement engagée dans ce qui fut appelée la Révolution de Jasmin. Son article non achevé, qui devait paraître dans ce volume, se serait ajouté à ses nombreuses autres publications dans le domaine de la socio-linguistique. Cette petite note rappellera la mémoire de celle qui fut non seulement une collègue, mais aussi une amie. Université Laval 3 Juillet 2013 Justin K. Bisanswa"""  # noqa
