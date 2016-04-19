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
