import pytest

from datetime import datetime
import typing

from eruditarticle.objects import EruditPublication, Title, SummaryArticle
from eruditarticle.tests.decorators import with_value, with_fixtures

from .test_article import people_to_dict

from ..objects.exceptions import InvalidTypercError, LiberuditarticleError


class Title(Title):
    def __init__(self, title=None, subtitle=None, lang=None):
        self.lang = lang
        self.title = title
        self.subtitle = subtitle


@with_fixtures(
    "./eruditarticle/tests/fixtures/publication/journal_title", EruditPublication
)
class TestCanReturnJournalTitle(object):
    @with_value("memoires03051.xml", "get_journal_title", formatted=True)
    def test_can_return_formatted_journal_title_with_paral_titles(self, value):
        assert value == "Mémoires du livre / Studies in Book Culture"

    @with_value("memoires03051.xml", "get_journal_title")
    def test_can_return_journal_title_with_paral_titles(self, value):
        assert value == {
            "main": Title(title="Mémoires du livre", subtitle=None, lang="fr"),
            "paral": [Title(title="Studies in Book Culture", subtitle=None, lang="en")],
            "equivalent": [],
        }

    @with_value("cine02589.xml", "get_journal_title", formatted=True)
    def test_can_format_journal_titles_and_subtitles(self, value):
        assert (
            value
            == "Cinémas\xa0: revue d'études cinématographiques / Cinémas: Journal of Film Studies"
        )  # noqa

    @with_value("cine02589.xml", "get_journal_title", formatted=True, subtitles=False)
    def test_can_format_journal_titles_without_subtitles(self, value):
        assert value == "Cinémas"

    @with_value("cine02589.xml", "get_journal_title")
    def test_can_return_journal_titles_and_subtitles(self, value):
        assert value == {
            "main": Title(
                title="Cinémas", subtitle="Revue d'études cinématographiques", lang="fr"
            ),
            "paral": [
                Title(title="Cinémas", subtitle="Journal of Film Studies", lang="en")
            ],
            "equivalent": [],
        }


@with_fixtures(
    "./eruditarticle/tests/fixtures/publication/volume_numbering", EruditPublication
)
class TestAbbreviatedPublicationVolumeNumbering(object):
    @with_value("cd02305.xml", "get_volume_numbering", formatted=True, abbreviated=True)
    def test_can_format_volume_and_number(self, value):
        assert value == "Vol. 56, n° 3-4, septembre–décembre 2015"

    @with_value(
        "annuaire3703.xml", "get_volume_numbering", formatted=True, abbreviated=True
    )
    def test_can_format_volume_numbering_horsserie_year(self, value):
        assert value == "N° hors-série, 2001"

    @with_value("haf2442.xml", "get_volume_numbering", formatted=True, abbreviated=True)
    def test_can_format_volume_numbering_in_case_of_index(self, value):
        assert value == "Index, 1997"

    @with_value(
        "sequences1128840.xml", "get_volume_numbering", formatted=True, abbreviated=True
    )
    def test_can_format_volume_numbering_no_volume_multiple_months(self, value):
        assert value == "N° 211, janvier–février 2001"

    @with_value(
        "sequences1081634.xml", "get_volume_numbering", formatted=True, abbreviated=True
    )
    def test_can_format_volume_numbering_in_case_of_index_with_number(self, value):
        assert value == "N° 125, index, 1986"

    @with_value(
        "inter1068986.xml", "get_volume_numbering", formatted=True, abbreviated=True
    )
    def test_can_format_volume_numbering_in_case_of_supplement(self, value):
        assert value == "N° 110, supplément, hiver 2012"

    @with_value(
        "ehr1825418.xml", "get_volume_numbering", formatted=True, abbreviated=True
    )
    def test_can_format_volume_publication_period(self, value):
        assert value == "Vol. 73, 2007"

    @with_value(
        "crs1517600.xml",
        "get_volume_numbering",
        formatted=True,
        abbreviated=True,
        html=True,
    )  # noqa
    def test_can_format_volume_numbering_in_case_of_horsserie(self, value):
        assert value == "N<sup>o</sup> hors-série, 2003"

    @with_value(
        "mcr82_83.xml",
        "get_volume_numbering",
        formatted=True,
        abbreviated=True,
        html=True,
    )
    def test_can_format_double_volumes(self, value):
        assert value == "Vol. 82-83, 2015–2016"

    @with_value(
        "sp04510.xml",
        "get_volume_numbering",
        formatted=True,
        abbreviated=True,
        html=True,
    )
    def test_empty_volume_and_number_do_not_crash(self, value):
        assert value == "2018"


@with_fixtures(
    "./eruditarticle/tests/fixtures/publication/volume_numbering", EruditPublication
)
class TestPublicationVolumeNumbering(object):
    @with_value("sp063.xml", "get_volume_numbering", formatted=True)
    def test_can_format_no_volume_no_number(self, value):
        assert value == "2016"

    @with_value("cd02305.xml", "get_volume_numbering", formatted=True)
    def test_can_format_volume_and_number(self, value):
        assert value == "Volume 56, numéro 3-4, septembre–décembre 2015"

    @with_value("annuaire3703.xml", "get_volume_numbering", formatted=True)
    def test_can_format_volume_numbering_horsserie_year(self, value):
        assert value == "Numéro hors-série, 2001"

    @with_value("haf2442.xml", "get_volume_numbering", formatted=True)
    def test_can_format_volume_numbering_in_case_of_index(self, value):
        assert value == "Index, 1997"

    @with_value("sequences1128840.xml", "get_volume_numbering", formatted=True)
    def test_can_format_volume_numbering_no_volume_multiple_months(self, value):
        assert value == "Numéro 211, janvier–février 2001"

    @with_value("sequences1081634.xml", "get_volume_numbering", formatted=True)
    def test_can_format_volume_numbering_in_case_of_index_with_number(self, value):
        assert value == "Numéro 125, index, 1986"

    @with_value("inter1068986.xml", "get_volume_numbering", formatted=True)
    def test_can_format_volume_numbering_in_case_of_supplement(self, value):
        assert value == "Numéro 110, supplément, hiver 2012"

    @with_value("ehr1825418.xml", "get_volume_numbering", formatted=True)
    def test_can_format_volume_publication_period(self, value):
        assert value == "Volume 73, 2007"

    @with_value("crs1517600.xml", "get_volume_numbering", formatted=True)
    def test_can_format_volume_numbering_in_case_of_horsserie(self, value):
        assert value == "Numéro hors-série, 2003"

    @with_value("va1503694.xml", "get_volume_numbering", formatted=True)
    def test_can_format_volume_number_numbertype(self, value):
        assert value == "Volume 52, numéro 214, supplément, printemps 2009"

    @with_value("as2866.xml", "get_volume_numbering", formatted=True)
    def test_can_format_volume_numbering_horsserie_no_number(self, value):
        assert value == "Volume 32, numéro hors-série, 2008"

    @with_value("as2866.xml", "get_volume_numbering")
    def test_can_return_unformatted_volume_numbering_horsserie_no_number(
        self, value
    ):  # noqa
        assert value == {
            "volume": "32",
            "number": "",
            "alt_number": "",
            "number_type": "hs",
            "publication_period": "2008",
        }


@with_fixtures(
    "./eruditarticle/tests/fixtures/publication/general_notes", EruditPublication
)
class TestEditorialNotes(object):
    @with_value("multilingual_edito.xml", "get_notegens_edito", html=True)
    def test_can_return_multilingual_note_html(self, value):
        assert value == [
            {
                "lang": "fr",
                "type": "edito",
                "content": '<p class="alinea">Ce numéro d’Eurostudia est publié avec l’aide de l’Office allemand d’échanges universitaires (DAAD) grâce au soutien financier du ministère des Affaires étrangères de la République fédérale d’Allemagne.</p>',  # noqa
                "authors": "",
            },
            {
                "lang": "de",
                "type": "edito",
                "content": '<p class="alinea">Hergestellt mit Unterstützung durch den DAAD aus Mitteln, die das Auswärtige Amt bereitstellt.</p>',  # noqa
                "authors": "",
            },
            {
                "lang": "en",
                "type": "edito",
                "content": '<p class="alinea">This issue of <em>Eurostudia</em> is published with the support of the German Academic Exchange Service (DAAD) thanks to financial assistance from the Foreign Office of the Federal Republic of Germany.</p>',  # noqa
                "authors": "",
            },
        ]

    @with_value("multilingual_edito.xml", "get_notegens_edito")
    def test_can_return_multilingual_note(self, value):
        assert value == [
            {
                "lang": "fr",
                "type": "edito",
                "content": "Ce numéro d’Eurostudia est publié avec l’aide de l’Office allemand d’échanges universitaires (DAAD) grâce au soutien financier du ministère des Affaires étrangères de la République fédérale d’Allemagne.",  # noqa
                "authors": "",
            },
            {
                "lang": "de",
                "type": "edito",
                "content": "Hergestellt mit Unterstützung durch den DAAD aus Mitteln, die das Auswärtige Amt bereitstellt.",  # noqa
                "authors": "",
            },
            {
                "lang": "en",
                "type": "edito",
                "content": "This issue of Eurostudia is published with the support of the German Academic Exchange Service (DAAD) thanks to financial assistance from the Foreign Office of the Federal Republic of Germany.",  # noqa
                "authors": "",
            },
        ]

    @with_value("rssi03944.xml", "get_notegens_edito")
    def test_can_return_multilingual_note_in_journal_languages_order(self, value):
        assert value == [
            {
                "lang": "fr",
                "type": "edito",
                "content": "Cette livraison de RS/SI couvre exceptionnellement deux volumes (vol. 35 nos. 2-3 et vol. 36 nos. 1-2). En vertu de notre entente avec la plateforme Erudit elle est présentée ici en deux tomes (Sémiotique du son au théâtre I et II) dont l’ensemble correspond à l’intégralité de la version imprimée.",  # noqa
                "authors": "",
            },
            {
                "lang": "en",
                "type": "edito",
                "content": "In Memoriam, Eli Rozik This publication of RS/SI exceptionally covers two volumes (vol. 35, nos. 2-3 and vol. 36 nos. 1-2). According to the terms of our agreement with the Erudit platform it is presented here in two tomes (Semiotics of Sound in Theatre I and II) which, together, correspond to the integrality of the printed version.",  # noqa
                "authors": "",
            },
        ]

    @with_value("edito_with_link.xml", "get_notegens_edito", html=True)
    def test_can_return_note_with_link_html(self, value):
        assert value == [
            {
                "lang": "fr",
                "type": "edito",
                "content": '<p class="alinea"><a href="http://www.erudit.org/projspec/ateliers/v10n2_complet.pdf">Télécharger le numéro complet / Download the complete issue</a></p>',  # noqa
                "authors": "",
            }
        ]

    @with_value("simple_edito.xml", "get_notegens_edito", html=True)
    def test_can_return_simple_note_html(self, value):
        assert value == [
            {
                "lang": "fr",
                "type": "edito",
                "content": '<p class="alinea">À la mémoire de Robert Plante, médecin du travail</p>',  # noqa
                "authors": "",
            }
        ]

    @with_value("simple_edito_with_link.xml", "get_notegens_edito", html=True)
    def test_can_return_simple_note_with_link_html(self, value):
        assert value == [
            {
                "lang": "fr",
                "type": "edito",
                "content": '<p class="alinea">Les textes qui composent ce numéro spécial de la <em>Revue de droit de McGill</em> se réfèrent à la présente introduction pour la présentation des faits de l’affaire et pour le résumé des jugements. Comme la plupart de ces textes sont en anglais, une version anglaise de cette introduction est disponible sur le site Web de la <em>Revue</em> (<a href="http://lawjournal.mcgill.ca">http://lawjournal.mcgill.ca</a>).</p>',  # noqa
                "authors": "",
            }
        ]

    @with_value("simple_edito_with_marquage.xml", "get_notegens_edito", html=True)
    def test_can_return_simple_note_with_marquage_html(self, value):
        assert value == [
            {
                "lang": "fr",
                "type": "edito",
                "content": '<p class="alinea"><strong>Remerciements :</strong> La Revue remercie le Bureau du Vice-rectorat à l’enseignement et à la recherche (Affaires francophones) de l’Université Laurentienne et l’Institut français de l’Université de Régina de leur appui financier à la production de ce numéro.</p>',  # noqa
                "authors": "",
            }
        ]

    @with_value("edito_in_liminaire.xml", "get_notegens_edito")
    def test_ignore_notegen_in_liminaire(self, value):
        # <notegen> tags in <liminaire> parent tag should *not* be considered in
        # get_notegens_edito(). edito_in_liminaire.xml contains such a tag ans we verify that it
        # doesn't end up in our results.
        assert value == []

    @with_value("rgd04541.xml", "get_notegens_edito")
    def test_ignore_notegen_when_scope_is_not_numero(self, value):
        assert value == []


@with_fixtures("./eruditarticle/tests/fixtures/publication", EruditPublication)
class TestPublicationPublisher(object):
    @with_value("ae1375.xml", "get_publishers")
    def test_can_return_a_single_publisher(self, value):
        assert value == [
            "HEC Montréal",
        ]


@with_fixtures("./eruditarticle/tests/fixtures/publication/editors", EruditPublication)
class TestPublicationEditors(object):
    @with_value("annuaire016.xml", "get_editors")
    def test_get_editors_should_return_regular_editors_but_not_guest_editors(
        self, value
    ):
        assert people_to_dict(value) == [
            {
                "affiliations": [],
                "othername": None,
                "firstname": "Louise",
                "email": None,
                "lastname": "Ladouceur",
                "organization": None,
                "role": {
                    "fr": "Rédactrice en chef",
                },
                "suffix": None,
            }
        ]

    @with_value("arbo02664.xml", "get_editors")
    def test_get_editors_should_not_return_guest_editors(self, value):
        assert value == []

    @with_value("ateliers02858.xml", "get_editors")
    def test_get_editors_should_return_all_regular_editors(self, value):
        assert people_to_dict(value) == [
            {
                "affiliations": [],
                "othername": None,
                "firstname": "Christine",
                "email": None,
                "lastname": "Tappolet",
                "organization": None,
                "role": {
                    "fr": "Rédactrice en chef",
                },
                "suffix": None,
            }
        ]


@with_fixtures("./eruditarticle/tests/fixtures/publication/themes", EruditPublication)
class TestPublicationFormattedThemes(object):
    @with_value("rmo20170401.xml", "get_themes", formatted=True, html=True)
    def test_can_return_theme_names_with_child_elements(self, value):
        assert value == [
            {
                "names": [
                    "Apprendre et enseigner la musique au XXI<sup>e</sup> siècle. Nouvelles propositions pédagogiques"
                ],  # noqa
                "editors": ["Francis Dubé"],
            }
        ]

    @with_value("smq1996211.xml", "get_themes", html=True, formatted=True)
    def test_can_display_multiple_themes_and_editors(self, value):
        assert value == [
            {"names": ["Virage ambulatoire"], "editors": ["Alain Lesage"]},
            {
                "names": ["Les états de stress post-traumatique"],
                "editors": ["Alain Lesage", "Louis Côté", "Yves Lecomte"],
            },
        ]

    @with_value("qf2012164.xml", "get_themes", html=True, formatted=True)
    def test_can_display_multiple_themes_and_multiple_editors(self, value):
        assert value == [
            {"names": ["L’actualité du mythe"], "editors": ["Vincent C. Lambert"]},
            {
                "names": ["Comprendre des textes à l’oral et à l’écrit"],
                "editors": ["Christian Dumais", "Réal Bergeron"],
            },
        ]

    @with_value("nps20121.xml", "get_themes", html=True, formatted=True)
    def test_can_display_multiple_themes_and_no_editors(self, value):
        assert value == [
            {
                "names": ["La prévention précoce en question"],
                "editors": [
                    "Michel Parazelli",
                    "Sylvie Lévesque",
                    "Carol Gélinas",
                ],
            },
            {"names": ["Regards croisés France-Québec"], "editors": []},
        ]

    @with_value("as20113512.xml", "get_themes", html=True, formatted=True)
    def test_can_display_paral_themes_and_editors(self, value):
        assert value == [
            {
                "names": [
                    "Cyberespace et anthropologie\xa0: transmission des savoirs et des savoir-faire",  # noqa
                    "Cyberspace and Anthropology\xa0: Transmission of Knowledge and Know-How",  # noqa
                    "Ciberespacio y antropologia\xa0: Transmision de conocimientos y de saber-como",  # noqa
                ],
                "editors": ["Joseph J. Lévy", "Évelyne Lasserre"],
            }
        ]

    @with_value("ttr03236.xml", "get_themes", html=True, formatted=True)
    def test_can_display_paral_themes_with_marquage(self, value):
        assert value == [
            {
                "editors": [
                    "Álvaro Echeverri",
                    "Georges L. Bastin",
                ],
                "names": [
                    "Territoires, histoires, mémoires",
                    "Territories, histories, memories",
                ],
            },
            {
                "editors": [
                    "Nicole Côté",
                    "Danièle Marcoux",
                    "Madeleine Stratford",
                ],
                "names": [
                    "La traduction littéraire <em>et</em> le Canada",
                    "Literary translation <em>and</em> Canada",
                ],
            },
        ]

    @with_value("circuit04198.xml", "get_themes", html=True, formatted=True)
    def test_theme_subname_first_letter_gets_lowercased(self, value):
        assert value == [
            {
                "editors": ["Luis Velasco-Pufleau"],
                "names": ["Engagements sonores\xa0: éthique et politique"],
            },
        ]

    @with_value("etudfr04537.xml", "get_themes", formatted=True, html=True)
    def test_spaces_between_xml_tags(self, value):
        assert value == [
            {
                "names": [
                    'Entre public et privé : lettres d’écrivains depuis le <span class="petitecap">xix</span><sup>e</sup> siècle'
                ],  # noqa
                "editors": ["Margot Irvine", "Karin Schwerdtner"],
            }
        ]

    @with_value("004966ar.xml", "get_themes", formatted=True, html=True)
    def test_empty_theme_tag(self, value):
        assert value == [
            {
                "names": [],
                "editors": [],
            }
        ]


@with_fixtures(
    "./eruditarticle/tests/fixtures/publication/redacteurchef", EruditPublication
)
class TestRedacteurChef(object):
    @with_value("ltp3991.xml", "get_redacteurchef", typerc="invite")
    def test_can_find_redacteurchef_when_no_theme(self, value):
        redacteurchef = value[0]
        assert len(value) == 1
        assert (
            redacteurchef.firstname == "Marc"
            and redacteurchef.lastname == "Dumas"
            and redacteurchef.typerc == "invite"
        )

    def test_raises_value_error_when_typerc_is_not_invite_or_regulier(self):
        with pytest.raises(InvalidTypercError):
            self.test_objects["ltp3991.xml"].get_redacteurchef(typerc="erreur")

    @with_value("ltp3991.xml", "get_redacteurchef", typerc="invite", formatted=True)
    def test_can_format_redacteurchef(self, value):
        redacteurchef = value[0]
        assert len(value) == 1
        assert redacteurchef == "Marc Dumas"

    @with_value("smq1826.xml", "get_redacteurchef", idrefs=["th1"])
    def test_can_return_redacteurchef_of_one_theme(self, value):
        assert len(value) == 1
        redacteurchef = value[0]
        assert redacteurchef.lastname == "Lesage"

    @with_value("smq1826.xml", "get_redacteurchef", idrefs=["th1", "th2"])
    def test_can_return_redacteurchef_of_two_themes(self, value):
        assert len(value) == 3

    @with_value("smq1826.xml", "get_redacteurchef", idrefs=[])
    def test_can_return_redacteurchef_of_publication_when_themes(self, value):
        assert len(value) == 1
        redacteurchef = value[0]
        assert redacteurchef.lastname == "Lesage (NUMÉRO)"
        assert redacteurchef.typerc == "regulier"

    @with_value("ltp02888.xml", "get_redacteurchef", typerc="invite", idrefs=[])
    def test_does_not_return_thematic_redacteurchef_when_no_themes_specified(
        self, value
    ):
        assert len(value) == 0

    def test_if_invalid_typerc_raises_invalidtypercerror_exception(self):
        with pytest.raises(InvalidTypercError):
            self.test_objects["ltp02888.xml"].get_redacteurchef(typerc="invalid")

    def test_invalidtypercerror_exception_message_when_invalid_typerc(self):
        try:
            self.test_objects["ltp02888.xml"].get_redacteurchef(typerc="invalid")
        except InvalidTypercError as e:
            assert str(e) == "Must be 'regulier' or 'invite'"


@with_fixtures("./eruditarticle/tests/fixtures/publication", EruditPublication)
class TestEruditPublication(object):
    @with_value("ela03987.xml", "get_summary_articles")
    def test_get_summary_articles(self, value: typing.List[SummaryArticle]):
        for article in value:
            assert article.urlpdf

    @pytest.mark.parametrize(
        "localidentifier,accessible",
        [
            ("009276ar", False),
            ("009277ar", False),
            ("009278ar", False),
            ("009279ar", True),
            ("009280ar", True),
            ("009282ar", True),
            ("009283ar", False),
            ("009284ar", True),
            ("009285ar", True),
            ("009286ar", True),
            ("009287ar", True),
            ("009288ar", True),
            ("009289ar", True),
            ("009290ar", True),
        ],
    )
    def test_can_determine_if_publication_is_allowed(self, localidentifier, accessible):
        summary_article = self.test_objects["etudinuit777.xml"].get_summary_article(
            localidentifier
        )
        assert summary_article.accessible == accessible

    def test_get_summary_article_can_raise_liberuditarticleerror(self):
        with pytest.raises(LiberuditarticleError):
            self.test_objects["etudinuit777.xml"].get_summary_article("error")

    @with_value("ae1375.xml", "get_article_count")
    def test_can_return_the_number_of_articles_of_this_publication(self, value):
        assert value == 10

    @with_value("ae1375.xml", "get_first_page")
    def test_can_return_the_first_page_of_the_publication(self, value):
        assert value == "5"

    @with_value("ae1375.xml", "get_last_page")
    def test_can_return_the_last_page_of_the_publication(self, value):
        assert value == "316"

    @with_value("hphi3180.xml", "get_first_page")
    def test_can_return_the_first_page_of_the_publication_when_first_page_in_roman_numerals(
        self, value
    ):  # noqa
        assert value == "III"

    @with_value("hphi3180.xml", "get_last_page")
    def test_can_return_the_last_page_of_the_publication_when_first_page_in_roman_numerals(
        self, value
    ):  # noqa
        assert value == "149"

    @with_value("spirale04246.xml", "get_first_page")
    def test_can_return_the_first_page_of_the_publication_when_articles_not_in_order(
        self, value
    ):
        assert value == "3"

    @with_value("spirale04246.xml", "get_last_page")
    def test_can_return_the_last_page_of_the_publication_when_articles_not_in_order(
        self, value
    ):
        assert value == "97"

    @with_value("teoros02917.xml", "get_first_page")
    def test_can_return_the_first_page_of_the_publication_when_no_pages(self, value):
        assert value is None

    @with_value("teoros02917.xml", "get_last_page")
    def test_can_return_the_last_page_of_the_publication_when_no_pages(self, value):
        assert value is None

    def test_number(self):
        assert self.test_objects["ae1375.xml"].get_number() == "1-2"
        assert self.test_objects["crs1517600.xml"].get_number() == ""
        assert self.test_objects["esse02315.xml"].get_number() == "86"

    def test_can_return_its_title(self):
        assert self.test_objects["ae1375.xml"].get_titles(html=False) == {
            "main": Title(title="L'Actualité économique", subtitle=None, lang="fr"),
            "paral": [],
            "equivalent": [],
        }

        assert self.test_objects["crs1517600.xml"].get_titles(html=False) == {
            "main": Title(
                title="Cahiers de recherche sociologique", subtitle=None, lang="fr"
            ),
            "paral": [],
            "equivalent": [],
        }

        assert self.test_objects["mje02648.xml"].get_titles(html=False) == {
            "main": Title(
                title="McGill Journal of Education", subtitle=None, lang="en"
            ),
            "paral": [
                Title(
                    title="Revue des sciences de l'éducation de McGill",
                    subtitle=None,
                    lang="fr",
                )
            ],  # noqa
            "equivalent": [],
        }

    @with_value("haf2442.xml", "get_publication_date")
    def test_can_return_its_publication_date_as_string(self, value):
        assert value == "2008-10-28"

    @with_value("haf2442.xml", "get_publication_date", as_datetime=True)
    def test_can_return_its_publication_date_as_date(self, value):
        assert value == datetime(year=2008, month=10, day=28)

    def test_can_return_its_publication_type(self):
        assert self.test_objects["haf2442.xml"].get_publication_type() == "index"
        assert self.test_objects["inter1068986.xml"].get_publication_type() == "supp"
        assert self.test_objects["crs1517600.xml"].get_publication_type() == "hs"

    def test_can_return_its_formatted_publication_type(self):
        assert (
            self.test_objects["haf2442.xml"].get_publication_type(formatted=True)
            == "index"
        )  # noqa
        assert (
            self.test_objects["inter1068986.xml"].get_publication_type(formatted=True)
            == "supplément"
        )  # noqa
        assert (
            self.test_objects["crs1517600.xml"].get_publication_type(formatted=True)
            == "hors-série"
        )  # noqa

    def test_themes(self):
        themes = self.test_objects["images1080663.xml"].get_themes()
        assert themes == {
            "th1": {
                "name": "David Cronenberg",
                "redacteurchef": [],
                "paral": {},
                "subname": None,
                "html_name": "David Cronenberg",
                "html_subname": None,
                "lang": "fr",
            },
            "th2": {
                "name": "La production au Québec",
                "redacteurchef": [],
                "paral": {},
                "subname": "Cinq cinéastes sur le divan",
                "html_name": "La production au Québec",
                "html_subname": "Cinq cinéastes sur le divan",
                "lang": "fr",
            },
        }

    def test_multiple_themes_multiple_redacteur(self):
        themes = self.test_objects["smq1826.xml"].get_themes()
        assert len(themes.keys()) == 2
        assert len(themes["th1"]["redacteurchef"]) == 1
        assert len(themes["th2"]["redacteurchef"]) == 3
        assert themes["th1"]["redacteurchef"][0].firstname == "Alain"
        assert themes["th1"]["redacteurchef"][0].lastname == "Lesage"

    def test_theme_paral(self):
        themes = self.test_objects["esse02315.xml"].get_themes()
        assert len(themes.keys()) == 1
        assert themes["th1"]["name"] == "Géopolitique"
        assert themes["th1"]["paral"]["en"] == {
            "name": "Geopolitics",
            "lang": "en",
            "subname": None,
            "html_name": "Geopolitics",
            "html_subname": None,
        }

    def test_sstheme(self):
        themes = self.test_objects["images1080663.xml"].get_themes()
        assert len(themes.keys()) == 2
        assert themes["th2"] == {
            "name": "La production au Québec",
            "paral": {},
            "redacteurchef": [],
            "subname": "Cinq cinéastes sur le divan",
            "html_name": "La production au Québec",
            "html_subname": "Cinq cinéastes sur le divan",
            "lang": "fr",
        }

    def test_redacteurchef(self):
        redacteurchef = self.test_objects["ae1375.xml"].get_redacteurchef()
        assert redacteurchef[0].firstname == "Olivier"
        assert redacteurchef[0].lastname == "Donni"
        assert redacteurchef[0].typerc == "invite"

        redacteurchef = self.test_objects[
            "images1102374.xml"
        ].get_redacteurchef()  # noqa
        assert redacteurchef[0].firstname == "Marie-Claude"
        assert redacteurchef[0].lastname == "Loiselle"
        assert redacteurchef[0].typerc == "regulier"

    def test_droitsauteur(self):
        assert self.test_objects["images1102374.xml"].get_droitsauteur() == [
            {"text": "Tous droits réservés © 24 images, 2000"}
        ]  # noqa
        assert self.test_objects["liberte1035607.xml"].get_droitsauteur() == [
            {"text": "Tous droits réservés © Collectif Liberté, 1993"}
        ]  # noqa
        assert self.test_objects["ritpu0326.xml"].get_droitsauteur()[0] == {
            "text": "Tous droits réservés © CRÉPUQ,"
        }  # noqa
        assert self.test_objects["ritpu0326.xml"].get_droitsauteur()[1] == {
            "href": "http://creativecommons.org/licenses/by-nc-sa/3.0/deed.fr_CA",
            "img": "http://i.creativecommons.org/l/by-nc-sa/3.0/88x31.png",
        }
        # Links only.
        assert self.test_objects["approchesind04155.xml"].get_droitsauteur(
            links_only=True
        ) == [
            {
                "href": "http://creativecommons.org/licenses/by-sa/3.0/",
                "img": "http://i.creativecommons.org/l/by-sa/3.0/88x31.png",
            }
        ]
        assert (
            self.test_objects["images1080663.xml"].get_droitsauteur(links_only=True)
            == []
        )

    def test_droitsauteurorg(self):
        assert (
            self.test_objects["images1102374.xml"].get_droitsauteurorg() == "24 images"
        )
        assert (
            self.test_objects["liberte1035607.xml"].get_droitsauteurorg()
            == "Collectif Liberté"
        )

    def test_notegen(self):
        assert self.test_objects["rum01069.xml"].get_notegens_edito(html=True) == [
            {
                "type": "edito",
                "lang": "fr",
                "content": """<p class="alinea"><strong>POUR NABIHA</strong> : Nabiha Jerad, Professeur de socio-linguistique à la Faculté des Lettres de l’Université de Tunis se trouvait dans son île natale, Kerkennah, pour célébrer le Ramadan avec sa famille. Sortie pour prendre l’air avant le dîner, elle fut renversée par une voiture. Le chauffeur - ou plutôt le chauffard - ne s’arrêta pas et s’enfuit. C’était le 11 août 2012. Elle tomba dans un coma dont elle ne se sortira jamais, malgré les soins intensifs et le dévouement du personnel médical, d’abord à Bruxelles, ensuite à Tunis où elle rendit l’âme le 19 octobre 2012. </p><p class="alinea">Pour ceux et celles qui l’ont connue, Nabiha avait le coeur sur la main, l’esprit ouvert à “tous les souffles du monde” pour reprendre Aimé Césaire. Elle était d’un grand dévouement envers ses étudiants, très attachée à son pays la Tunisie et fortement engagée dans ce qui fut appelée la Révolution de Jasmin. Son article non achevé, qui devait paraître dans ce volume, se serait ajouté à ses nombreuses autres publications dans le domaine de la socio-linguistique. Cette petite note rappellera la mémoire de celle qui fut non seulement une collègue, mais aussi une amie. Université Laval 3 Juillet 2013</p>""",  # noqa
                "authors": "Justin K. Bisanswa",
            }
        ]
        assert self.test_objects["rum01069.xml"].get_notegens_edito() == [
            {
                "type": "edito",
                "lang": "fr",
                "content": """POUR NABIHA : Nabiha Jerad, Professeur de socio-linguistique à la Faculté des Lettres de l’Université de Tunis se trouvait dans son île natale, Kerkennah, pour célébrer le Ramadan avec sa famille. Sortie pour prendre l’air avant le dîner, elle fut renversée par une voiture. Le chauffeur - ou plutôt le chauffard - ne s’arrêta pas et s’enfuit. C’était le 11 août 2012. Elle tomba dans un coma dont elle ne se sortira jamais, malgré les soins intensifs et le dévouement du personnel médical, d’abord à Bruxelles, ensuite à Tunis où elle rendit l’âme le 19 octobre 2012. Pour ceux et celles qui l’ont connue, Nabiha avait le coeur sur la main, l’esprit ouvert à “tous les souffles du monde” pour reprendre Aimé Césaire. Elle était d’un grand dévouement envers ses étudiants, très attachée à son pays la Tunisie et fortement engagée dans ce qui fut appelée la Révolution de Jasmin. Son article non achevé, qui devait paraître dans ce volume, se serait ajouté à ses nombreuses autres publications dans le domaine de la socio-linguistique. Cette petite note rappellera la mémoire de celle qui fut non seulement une collègue, mais aussi une amie. Université Laval 3 Juillet 2013""",  # noqa
                "authors": "Justin K. Bisanswa",
            }
        ]

    def test_issn(self):
        assert self.test_objects["ae1375.xml"].issn == "0001-771X"

    def test_issn_num(self):
        assert self.test_objects["ae1375.xml"].issn_num == "1710-3991"

    def test_isbn(self):
        assert self.test_objects["crs1517600.xml"].isbn == "2-89578-037-4"
        assert self.test_objects["inter02349.xml"].isbn == "978-2-924298-19-0"
        assert self.test_objects["esse02315.xml"].isbn is None

    def test_isbn_num(self):
        assert self.test_objects["esse02315.xml"].isbn_num == "978-2-924345-09-2"
        assert self.test_objects["inter02349.xml"].isbn_num == "978-2-924298-20-6"
        assert self.test_objects["crs1517600.xml"].isbn_num is None

    def test_note_edito(self):
        assert self.test_objects["rum01069.xml"].note_edito.startswith("POUR NABIHA")
        assert self.test_objects["rum01069.xml"].note_edito.endswith("Bisanswa")

    def test_guest_editors(self):
        assert people_to_dict(self.test_objects["ae1375.xml"].guest_editors) == [
            {
                "affiliations": [],
                "othername": None,
                "firstname": "Olivier",
                "email": None,
                "lastname": "Donni",
                "organization": None,
                "role": {},
                "suffix": None,
            }
        ]

    def test_directors(self):
        assert people_to_dict(self.test_objects["ae1375.xml"].directors) == [
            {
                "affiliations": [],
                "othername": None,
                "firstname": "Patrick",
                "email": None,
                "lastname": "González",
                "organization": None,
                "role": {},
                "suffix": None,
            }
        ]

        assert people_to_dict(self.test_objects["haf2442.xml"].directors) == [
            {
                "affiliations": [],
                "othername": None,
                "firstname": "Fernande",
                "email": None,
                "lastname": "Roy",
                "organization": None,
                "role": {"fr": "Directrice"},
                "suffix": None,
            }
        ]

        assert "en" not in self.test_objects["haf2442.xml"].directors[0].role

    def test_editors(self):
        assert people_to_dict(self.test_objects["images1080663.xml"].editors) == [
            {
                "affiliations": [],
                "othername": None,
                "firstname": "Isabelle",
                "lastname": "Richer",
                "email": None,
                "organization": None,
                "role": {"fr": "Rédactrice adjointe"},
                "suffix": None,
            }
        ]

    def test_can_find_roles_in_all_languages(self):
        directors = self.test_objects["haf2442-alt.xml"].directors
        assert len(directors) == 1
        director = directors[0]
        assert director.role == {"es": "Directrice"}

    def test_roles_are_associated_with_the_proper_person(self):
        """ Test that an editor only has his own roles """
        editors = self.test_objects["mje02648.xml"].editors
        editor = editors[0]

        assert editor.lastname == "Strong-Wilson"
        assert "fr" not in editor.role
        assert editor.role["en"] == "Editor-in-Chief / Rédactrice-en-chef"

    def test_publication_period_doesnt_crash(self):
        # Don't crash when we can't find a publication period. Return an empty value.
        pub = self.test_objects["ae1375.xml"]
        elem = pub.find("numero/pub")
        del elem[:]
        assert pub.get_publication_period() == ""

    def test_get_volume_numbering_with_alternative_number(self):
        assert self.test_objects["vi04327.xml"].get_volume_numbering() == {
            "volume": "44",
            "number": "1",
            "alt_number": "130",
            "number_type": "reg",
            "publication_period": "Automne 2018",
        }
        assert (
            self.test_objects["vi04327.xml"].get_volume_numbering(formatted=True)
            == "Volume 44, numéro 1 (130), automne 2018"
        )  # noqa
        assert (
            self.test_objects["vi04327.xml"].get_volume_numbering(
                abbreviated=True, formatted=True
            )
            == "Vol. 44, n° 1 (130), automne 2018"
        )  # noqa

    def test_get_volume_numbering_with_alternative_number_and_no_number(self):
        assert self.test_objects["scientia3124.xml"].get_volume_numbering() == {
            "volume": "24",
            "number": "",
            "alt_number": "52",
            "number_type": None,
            "publication_period": "2000",
        }
        assert (
            self.test_objects["scientia3124.xml"].get_volume_numbering(formatted=True)
            == "Volume 24, numéro 52, 2000"
        )  # noqa
        assert (
            self.test_objects["scientia3124.xml"].get_volume_numbering(
                abbreviated=True, formatted=True
            )
            == "Vol. 24, n° 52, 2000"
        )  # noqa

    def test_volume_numbering_doesnt_crash(self):
        # Don't crash when get_volume_numbering() is missing all info it needs to return something
        # at all. just return an empty string.
        pub = self.test_objects["ae1375.xml"]
        elem = pub.find("numero")
        del elem[:]
        assert pub.get_volume_numbering(formatted=True) == ""

    @pytest.mark.parametrize(
        "fixture, language, html, expected_label",
        [
            ("images1080663.xml", "fr", True, "Tous droits réservés"),
            ("images1080663.xml", "en", True, "All Rights Reserved"),
            ("images1080663.xml", "es", True, "Reservados todos los derechos"),
            ("images1080663.xml", "fr", False, "Tous droits réservés"),
            ("images1080663.xml", "en", False, "All Rights Reserved"),
            ("images1080663.xml", "es", False, "Reservados todos los derechos"),
            # Unavailable language, defaults to first label.
            ("images1080663.xml", "zz", False, "Tous droits réservés"),
            # Missing label.
            ("ae1806445.xml", "fr", True, ""),
            ("ae1806445.xml", "fr", False, ""),
        ],
    )
    def test_get_copyrights_label(self, fixture, language, html, expected_label):
        publication = self.test_objects[fixture]
        assert (
            publication._get_copyrights_label(
                publication.find("copyright"), language, html=html
            )
            == expected_label
        )  # noqa

    @pytest.mark.parametrize(
        "fixture, html, expected_names",
        [
            ("images1080663.xml", True, ["24 images inc."]),
            ("images1080663.xml", False, ["24 images inc."]),
            # Missing names.
            ("moebius1016931.xml", True, []),
            ("moebius1016931.xml", False, []),
            # Multiple names, including physical person with prefix.
            ("liberte1032075.xml", False, ["Mme E. Bertil", "Collectif Liberté"]),
            ("liberte1032075.xml", True, ["Mme E. Bertil", "Collectif Liberté"]),
        ],
    )
    def test_get_copyrights_names(self, fixture, html, expected_names):
        publication = self.test_objects[fixture]
        assert (
            publication._get_copyrights_names(publication.find("copyright"), html=html)
            == expected_names
        )  # noqa

    @pytest.mark.parametrize(
        "fixture, html, expected_year",
        [
            ("images1080663.xml", True, "1992"),
            ("images1080663.xml", False, "1992"),
            # Missing year.
            ("va1258133.xml", True, ""),
            ("va1258133.xml", False, ""),
        ],
    )
    def test_get_copyrights_year(self, fixture, html, expected_year):
        publication = self.test_objects[fixture]
        assert (
            publication._get_copyrights_year(publication.find("copyright"), html=html)
            == expected_year
        )  # noqa

    @pytest.mark.parametrize(
        "fixture, language, formatted, html, expected_copyrights",
        [
            (
                "images1080663.xml",
                "fr",
                False,
                False,
                {
                    "label": "Tous droits réservés",
                    "names": ["24 images inc."],
                    "year": "1992",
                },
            ),  # noqa
            (
                "images1080663.xml",
                "en",
                False,
                False,
                {
                    "label": "All Rights Reserved",
                    "names": ["24 images inc."],
                    "year": "1992",
                },
            ),  # noqa
            (
                "images1080663.xml",
                "es",
                False,
                False,
                {
                    "label": "Reservados todos los derechos",
                    "names": ["24 images inc."],
                    "year": "1992",
                },
            ),  # noqa
            (
                "images1080663.xml",
                "fr",
                True,
                False,
                "Tous droits réservés © 24 images inc., 1992",
            ),
            (
                "images1080663.xml",
                "en",
                True,
                False,
                "All Rights Reserved © 24 images inc., 1992",
            ),
            (
                "images1080663.xml",
                "es",
                True,
                False,
                "Reservados todos los derechos © 24 images inc., 1992",
            ),  # noqa
            (
                "images1080663.xml",
                "fr",
                False,
                True,
                "Tous droits réservés © 24 images inc., 1992",
            ),  # noqa
            (
                "images1080663.xml",
                "en",
                False,
                True,
                "All Rights Reserved © 24 images inc., 1992",
            ),
            (
                "images1080663.xml",
                "es",
                False,
                True,
                "Reservados todos los derechos © 24 images inc., 1992",
            ),  # noqa
            # Unavailable language, defaults to first label.
            (
                "images1080663.xml",
                "zz",
                False,
                False,
                {
                    "label": "Tous droits réservés",
                    "names": ["24 images inc."],
                    "year": "1992",
                },
            ),  # noqa
            # Missing label.
            (
                "ae1806445.xml",
                "fr",
                False,
                False,
                {"label": "", "names": ["HEC Montréal"], "year": "1970"},
            ),  # noqa
            ("ae1806445.xml", "fr", True, False, " © HEC Montréal, 1970"),
            ("ae1806445.xml", "fr", False, True, " © HEC Montréal, 1970"),
            # Missing names.
            (
                "moebius1016931.xml",
                "fr",
                False,
                False,
                {"label": "Tous droits réservés", "names": [], "year": "1997"},
            ),  # noqa
            ("moebius1016931.xml", "fr", True, False, "Tous droits réservés © , 1997"),
            ("moebius1016931.xml", "fr", False, True, "Tous droits réservés © , 1997"),
            # Missing year.
            (
                "va1258133.xml",
                "fr",
                False,
                False,
                {
                    "label": "Tous droits réservés",
                    "names": ["La Société des Arts"],
                    "year": "",
                },
            ),  # noqa
            (
                "va1258133.xml",
                "fr",
                True,
                False,
                "Tous droits réservés © La Société des Arts, ",
            ),
            (
                "va1258133.xml",
                "fr",
                False,
                True,
                "Tous droits réservés © La Société des Arts, ",
            ),  # noqa
            # Multiple names, including physical person with prefix.
            (
                "liberte1032075.xml",
                "fr",
                False,
                False,
                {
                    "label": "Tous droits réservés",
                    "names": ["Mme E. Bertil", "Collectif Liberté"],
                    "year": "1986",
                },
            ),  # noqa
            (
                "liberte1032075.xml",
                "fr",
                True,
                False,
                "Tous droits réservés © Mme E. Bertil et Collectif Liberté, 1986",
            ),  # noqa
            (
                "liberte1032075.xml",
                "fr",
                False,
                True,
                "Tous droits réservés © Mme E. Bertil et Collectif Liberté, 1986",
            ),  # noqa
        ],
    )
    def test_get_copyrights(
        self, fixture, language, formatted, html, expected_copyrights
    ):
        assert (
            self.test_objects[fixture].get_copyrights(
                language, formatted=formatted, html=html
            )
            == expected_copyrights
        )  # noqa

    @pytest.mark.parametrize(
        "names, expected_result",
        [
            ([], ""),
            (["Foo"], "Foo"),
            (["Foo", "Bar"], "Foo et Bar"),
            (["Foo", "Bar", "Baz"], "Foo, Bar et Baz"),
        ],
    )
    def test_format_names(self, names, expected_result):
        assert (
            self.test_objects["images1080663.xml"]._format_names(names)
            == expected_result
        )

    def test_get_languages(self):
        # Languages are specified on the <revue> element, we should get them as a list.
        assert self.test_objects["esse02315.xml"].get_languages() == ["fr", "en"]
        # No languages are specified on the <revue> element, defaults to ['fr'].
        assert self.test_objects["hphi3180.xml"].get_languages() == ["fr"]
