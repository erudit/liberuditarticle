
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
        assert self.test_objects['images1102374.xml'].get_droitauteur() == "Tous droits réservés © 24 images, 2000"
        assert self.test_objects['liberte1035607.xml'].get_droitauteur() == "Tous droits réservés © Collectif Liberté, 1993"

    def test_droitauteurorg(self):
        assert self.test_objects['images1102374.xml'].get_droitauteurorg() == "24 images"
        assert self.test_objects['liberte1035607.xml'].get_droitauteurorg() == "Collectif Liberté"

    #def test_isbn(self):
    #    assert self.test_objects['images1102374.xml'].get_isbn() == '2-922607-82-8'
