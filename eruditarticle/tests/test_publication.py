from datetime import datetime
from eruditarticle.objects.base import Title
from eruditarticle.objects import EruditPublication
from eruditarticle.tests.decorators import with_value, with_fixtures


@with_fixtures('./eruditarticle/tests/fixtures/publication/volume_numbering', EruditPublication)
class TestAbbreviatedPublicationVolumeNumbering(object):

    @with_value("cd02305.xml", "get_volume_numbering", formatted=True, abbreviated=True)
    def test_can_format_volume_and_number(self, value):
        assert value == "Vol. 56, n° 3-4, septembre–décembre 2015"

    @with_value("annuaire3703.xml", "get_volume_numbering", formatted=True, abbreviated=True)
    def test_can_format_volume_numbering_horsserie_year(self, value):
        assert value == "N° hors-série, 2001"

    @with_value("haf2442.xml", "get_volume_numbering", formatted=True, abbreviated=True)
    def test_can_format_volume_numbering_in_case_of_index(self, value):
        assert value == "Index, 1997"

    @with_value("sequences1128840.xml", "get_volume_numbering", formatted=True, abbreviated=True)
    def test_can_format_volume_numbering_no_volume_multiple_months(self, value):
        assert value == "N° 211, janvier–février 2001"

    @with_value("sequences1081634.xml", "get_volume_numbering", formatted=True, abbreviated=True)
    def test_can_format_volume_numbering_in_case_of_index_with_number(self, value):
        assert value == "N° 125, index, 1986"

    @with_value("inter1068986.xml", "get_volume_numbering", formatted=True, abbreviated=True)
    def test_can_format_volume_numbering_in_case_of_supplement(self, value):
        assert value == "N° 110, supplément, hiver 2012"

    @with_value("ehr1825418.xml", "get_volume_numbering", formatted=True, abbreviated=True)
    def test_can_format_volume_publication_period(self, value):
        assert value == "Vol. 73, 2007"

    @with_value("crs1517600.xml", "get_volume_numbering", formatted=True, abbreviated=True, html=True)  # noqa
    def test_can_format_volume_numbering_in_case_of_horsserie(self, value):
        assert value == "N<sup>o</sup> hors-série, 2003"


@with_fixtures('./eruditarticle/tests/fixtures/publication/volume_numbering', EruditPublication)
class TestPublicationVolumeNumbering(object):

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


@with_fixtures('./eruditarticle/tests/fixtures/publication', EruditPublication)
class TestPublicationPublisher(object):

    @with_value('ae1375.xml', 'get_publishers')
    def test_can_return_a_single_publisher(self, value):
        assert value == ['HEC Montréal', ]


@with_fixtures('./eruditarticle/tests/fixtures/publication/editors', EruditPublication)
class TestPublicationEditors(object):

    @with_value('annuaire016.xml', 'get_editors')
    def test_get_editors_should_return_regular_editors_but_not_guest_editors(self, value):
        assert value == [{
            'affiliations': [],
            'othername': None,
            'firstname': 'Louise',
            'email': None,
            'lastname': 'Ladouceur',
            'organization': None,
            'role': {
                'fr': 'Rédactrice en chef',
            },
            'suffix': None,
        }]

    @with_value('arbo02664.xml', 'get_editors')
    def test_get_editors_should_not_return_guest_editors(self, value):
        assert value == []

    @with_value('ateliers02858.xml', 'get_editors')
    def test_get_editors_should_return_all_regular_editors(self, value):
        assert value == [{
            'affiliations': [],
            'othername': None,
            'firstname': 'Christine',
            'email': None,
            'lastname': 'Tappolet',
            'organization': None,
            'role': {
                'fr': 'Rédactrice en chef',
            },
            'suffix': None,
        }]


@with_fixtures('./eruditarticle/tests/fixtures/publication/themes', EruditPublication)
class TestPublicationFormattedThemes(object):

    @with_value('rmo20170401.xml', 'get_themes', formatted=True, html=True)
    def test_can_return_theme_names_with_child_elements(self, value):
        assert value == [
            {
                'names': ["Apprendre et enseigner la musique au XXI<sup>e</sup> si&#232;cle. Nouvelles propositions p&#233;dagogiques"],  # noqa
                'editors': ["Francis Dub&#233;"],
            }
        ]

    @with_value('smq1996211.xml', 'get_themes', html=True, formatted=True)
    def test_can_display_multiple_themes_and_editors(self, value):
        assert value == [
            {
                'names': ["Virage ambulatoire"],
                'editors': ["Alain Lesage"]
            },
            {
                'names': ["Les &#233;tats de stress post-traumatique"],
                "editors": ["Alain Lesage", "Louis C&#244;t&#233;", "Yves Lecomte"]
            }
        ]

    @with_value('qf2012164.xml', 'get_themes', html=True, formatted=True)
    def test_can_display_multiple_themes_and_multiple_editors(self, value):
        assert value == [
            {
                'names': ["L&#8217;actualit&#233; du mythe"],
                'editors': ['Vincent C. Lambert']
            },
            {
                'names': ["Comprendre des textes &#224; l&#8217;oral et &#224; l&#8217;&#233;crit"],
                "editors": [
                    "Christian Dumais",
                    "R&#233;al Bergeron"
                ]
            }
        ]

    @with_value('nps20121.xml', 'get_themes', html=True, formatted=True)
    def test_can_display_multiple_themes_and_no_editors(self, value):
        assert value == [
            {
                'names': ["La pr&#233;vention pr&#233;coce en question"],
                "editors": [
                    "Michel Parazelli",
                    "Sylvie L&#233;vesque",
                    "Carol G&#233;linas",
                ]
            },
            {
                'names': ["Regards crois&#233;s France-Qu&#233;bec"],
                "editors": []
            }
        ]

    @with_value('as20113512.xml', 'get_themes', html=True, formatted=True)
    def test_can_display_paral_themes_and_editors(self, value):
        assert value == [
            {
                'names': [
                    "Cyberespace et anthropologie : transmission des savoirs et des savoir-faire",  # noqa
                    "Cyberspace and Anthropology : Transmission of Knowledge and Know-How",  # noqa
                    "Ciberespacio y antropologia : Transmision de conocimientos y de saber-como",  # noqa
                ],
                'editors': [
                    "Joseph J. L&#233;vy",
                    "&#201;velyne Lasserre"
                ]
            }
        ]

    # @with_value('ltp2010663.xml', 'get_themes', html=True, formatted=True)
    # def test_can_display_no_theme_and_guest_editor(self, value):
    #    assert value == [
    #        {'name': None, 'editors': 'Marc Dumas'}
    #    ]

    # @with_value('dss201092.xml', 'get_themes', html=True, formatted=True)
    # def test_can_display_no_theme_and_multiple_guest_editors(self, value):
    #     assert value == [
    #         {'name': None, 'editors': 'Pierre Lauzon et Michel Landry'}
    #     ]


@with_fixtures('./eruditarticle/tests/fixtures/publication/redacteurchef', EruditPublication)
class TestRedacteurChef(object):

    @with_value("ltp3991.xml", "get_redacteurchef", type="invite")
    def test_can_find_redacteurchef_when_no_theme(self, value):
        redacteurchef = value[0]
        assert len(value) == 1
        assert redacteurchef['firstname'] == 'Marc' and \
            redacteurchef['lastname'] == 'Dumas' and \
            redacteurchef['type'] == 'invite'


@with_fixtures('./eruditarticle/tests/fixtures/publication', EruditPublication)
class TestEruditPublication(object):

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

    @with_value("haf2442.xml", "get_publication_date")
    def test_can_return_its_publication_date_as_string(self, value):
        assert value == "2008-10-28"

    @with_value("haf2442.xml", "get_publication_date", as_datetime=True)
    def test_can_return_its_publication_date_as_date(self, value):
        assert value == datetime(year=2008, month=10, day=28)

    def test_can_return_its_publication_type(self):
        assert self.test_objects["haf2442.xml"].get_publication_type() == 'index'
        assert self.test_objects["inter1068986.xml"].get_publication_type() == 'supp'
        assert self.test_objects["crs1517600.xml"].get_publication_type() == 'hs'

    def test_can_return_its_formatted_publication_type(self):
        assert self.test_objects["haf2442.xml"].get_publication_type(formatted=True) == 'index'  # noqa
        assert self.test_objects["inter1068986.xml"].get_publication_type(formatted=True) == 'supplément'  # noqa
        assert self.test_objects["crs1517600.xml"].get_publication_type(formatted=True) == 'hors-série'  # noqa

    def test_themes(self):
        themes = self.test_objects["images1080663.xml"].get_themes()
        assert themes == {
            'th1': {
                'name': 'David Cronenberg',
                'redacteurchef': [],
                'paral': {},
                'subname': None,
                'html_name': 'David Cronenberg',
                'html_subname': None,
                'lang': 'fr',
            },
            'th2': {
                'name': 'La production au Québec',
                'redacteurchef': [],
                'paral': {},
                'subname': 'Cinq cinéastes sur le divan',
                'html_name': 'La production au Qu&#233;bec',
                'html_subname': 'Cinq cin&#233;astes sur le divan',
                'lang': 'fr',
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
            'name': 'Geopolitics', 'subname': None, 'html_name': 'Geopolitics',
            'html_subname': None, }

    def test_sstheme(self):
        themes = self.test_objects['images1080663.xml'].get_themes()
        assert len(themes.keys()) == 2
        assert themes['th2'] == {
            'name': 'La production au Québec',
            'paral': {},
            'redacteurchef': [],
            'subname': 'Cinq cinéastes sur le divan',
            'html_name': 'La production au Qu&#233;bec',
            'html_subname': 'Cinq cin&#233;astes sur le divan',
            'lang': 'fr',
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
