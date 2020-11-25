import pytest

from eruditarticle.objects import EruditJournal
from eruditarticle.tests.decorators import with_fixtures
from eruditarticle.tests.decorators import with_value


@with_fixtures("./eruditarticle/tests/fixtures/journal", EruditJournal)
class TestEruditJournal(object):
    def test_can_return_first_publication_year(self):
        assert self.test_objects["mi115.xml"].get_first_publication_year() == "2009"

    def test_can_return_last_publication_year(self):
        assert self.test_objects["mi115.xml"].get_last_publication_year() == "2015"

    def test_can_return_publication_period(self):
        assert self.test_objects["mi115.xml"].get_publication_period() == "2009 - 2015"

    def test_can_return_publication_years(self):
        assert self.test_objects["mi115.xml"].get_publication_years() == [
            "2009",
            "2010",
            "2011",
            "2012",
            "2013",
            "2014",
            "2015",
        ]

    @with_value("mi115.xml", "get_published_issues_pids")
    def test_can_return_list_of_published_issues_pids(self, value):
        assert len(value) == 29
        assert value[:2] == [
            "erudit:erudit.mi115.mi01857",
            "erudit:erudit.mi115.mi01686",
        ]
        assert value[::-1][:2] == [
            "erudit:erudit.mi115.mi2897",
            "erudit:erudit.mi115.mi3333",
        ]

    @with_value("mi115.xml", "get_last_published_issue_pid")
    def test_can_return_last_published_issue_pid(self, value):
        assert value == "erudit:erudit.mi115.mi01857"

    def test_can_return_journal_name(self):
        assert (
            self.test_objects["mi115.xml"].get_title()
            == "Management international / International Management / Gestiòn Internacional"
        )  # noqa

    def test_can_return_journal_notes(self):
        assert self.test_objects["phyto71.xml"].get_notes() == {
            "fr": [
                "Veuillez prendre note que des articles peuvent s'ajouter au dernier numéro en cours d'année",  # noqa
            ],
        }

    @with_value("recma0448.xml", "get_notes", html=True)
    def test_note_conversion(self, value):
        assert (
            value["fr"][0]
            == "Cette revue a cessé de publier ses numéros sur Érudit depuis "
            "2016, vous pouvez consulter les numéros subséquents sur "
            '<a href="https://www.cairn.info/revue-recma.htm">'
            "Cairn</a>"
        )

    @with_value("ravon92.xml", "get_notes", html=True)
    def test_get_notes_html(self, value):
        assert self.test_objects["ravon92.xml"].get_notes(html=True) == {
            "fr": [
                "Les publications précédentes (du numéro 1 au numéro 46) sont disponibles sur la pa"
                'ge de la revue <a href="https://www.erudit.org/fr/revues/ron">RON</a>. Les publica'
                "tions précédentes (du numéro 47 au numéro 67) sont disponibles sur la page de la r"
                'evue <a href="https://www.erudit.org/fr/revues/ravon/">RAVON</a>.',
                "Les publications précédentes (du numéro 1 au numéro 46) sont disponibles sur la pa"
                'ge de la revue <a href="https://www.erudit.org/fr/revues/ron">RON</a>. Les publica'
                "tions suivantes (à partir du numéro 68-69) sont disponibles sur la page de la nouv"
                'elle revue <a href="https://www.erudit.org/fr/revues/ronbrit">RON</a>.',
                "Les publications suivantes (du numéro 47 au numéro 67) sont disponibles sur la pag"
                'e de la revue <a href="https://www.erudit.org/fr/revues/ravon/">RAVON</a>. Les pub'
                "lications suivantes (à partir du numéro 68-69) sont disponibles sur la page de la "
                'nouvelle revue <a href="https://www.erudit.org/fr/revues/ronbrit">RON</a>.',
            ]
        }

    @pytest.mark.parametrize(
        "journal_pid, expected_result",
        (
            ("erudit:erudit.approchesind0522", {}),
            (
                "erudit:erudit.enjeux04890",
                {
                    "fr": [
                        "Les publications précédentes (du volume 1, numéro 1 au volume 6, numéro 1) sont "
                        "disponibles sur la page de la revue Approches inductives",
                    ]
                },
            ),
        ),
    )
    def test_can_return_journal_notes_for_given_journal_pid(
        self, journal_pid, expected_result
    ):
        journal = self.test_objects["approchesind0522.xml"]
        assert journal.get_notes(journal_pid=journal_pid) == expected_result

    @with_value("mi115.xml", "has_published_issues")
    def test_has_published_issues(self, value):
        assert value

    @with_value("captures04164.xml", "has_published_issues")
    def test_has_no_published_issues(self, value):
        assert not value
