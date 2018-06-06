import collections
import pytest
from lxml.builder import E

from eruditarticle.objects import EruditArticle
from eruditarticle.tests.decorators import with_value, with_fixtures


def person_to_dict(person):
    KEYS = {
        'firstname', 'lastname', 'othername', 'suffix', 'affiliations', 'email', 'organization',
        'role'}
    return {key: getattr(person, key) for key in KEYS}


def people_to_dict(people):
    return list(map(person_to_dict, people))


@with_fixtures('./eruditarticle/tests/fixtures/article/abstracts', EruditArticle)
class TestGetAbstracts:

    @with_value('1037207ar.xml', 'get_abstracts')
    def test_can_return_abstract_typeresume(self, value):
        assert value[0]['typeresume'] == 'resume'
        assert value[0]['content'] != ''

    @with_value('1043568ar.xml', 'get_abstracts')
    def test_can_return_abstracts_in_any_language(self, value):
        assert value[0]['type'] == 'main'
        assert value[0]['content'] != ''
        assert len(value) == 3
        assert len([a for a in value if a['type'] == 'equivalent']) == 2

    @with_value('1043568ar.xml', 'get_abstracts', html=True)
    def test_can_return_html_tags_of_abstracts(self, value):
        assert value[0]['type'] == 'main'
        assert value[0]['content'] == """<p><em>En fin de premi&#232;re ann&#233;e de formation &#224; l&#8217;enseignement primaire, les &#233;tudiants du canton de Vaud en Suisse sont certifi&#233;s par des examens de diff&#233;rentes natures. Pour cette recherche &#224; caract&#232;re exploratoire, nous avons retenu deux certifications particuli&#232;res. La premi&#232;re concerne un module intitul&#233; </em>Savoirs math&#233;matiques et enseignement<em>, qui est certifi&#233; par un questionnaire &#224; choix multiples (QCM) et qui exige des &#233;tudiants non seulement qu&#8217;ils r&#233;pondent aux questions, mais &#233;galement qu&#8217;ils indiquent leurs degr&#233;s de certitude des r&#233;ponses donn&#233;es. Ce faisant, ils s&#8217;auto&#233;valuent et cette estimation est prise en compte dans la r&#233;ussite &#224; l&#8217;examen. La seconde concerne un module intitul&#233; </em>Enseignement et apprentissage<em>. L&#8217;examen se structure par des questions ouvertes testant les capacit&#233;s d&#8217;analyse de t&#226;ches distribu&#233;es aux &#233;l&#232;ves des classes de la r&#233;gion. L&#8217;article pr&#233;sente les r&#233;sultats d&#8217;une recherche visant &#224; comprendre les liens entre des exp&#233;riences &#233;valuatives et des postures en formation de quatre &#233;tudiantes, puis &#224; d&#233;finir d&#8217;&#233;ventuelles logiques de formation. Nous avons relev&#233; quatre postures qui remettent en question le rapport aux savoirs de la profession.</em></p>"""  # noqa

    @with_value('1043568ar.xml', 'get_abstracts')
    def test_can_return_paral_abstracts_in_the_lang_order_defined_in_the_article(self, value):  # noqa
        equivalent_abstracts = [a for a in value if a['type'] == 'equivalent']
        assert [a['lang'] for a in equivalent_abstracts] == ["en", "pt"]

    @with_value('1043074ar.xml', 'get_abstracts')
    def test_will_always_return_main_abstract_first(self, value):
        assert [a['lang'] for a in value] == ['en', 'fr', 'es']

    @with_value('031125ar.xml', 'get_abstracts')
    def test_can_return_abstract_title(self, value):
        assert value[0] is not None
        assert value[0]['content'] != ''
        assert value[0]['title'] == 'Abstract'

    @with_value('1039501ar.xml', 'get_abstracts')
    def test_can_return_abstract_of_tei_articles(self, value):
        assert value[0] is not None
        assert value[0]['content'] != ''


@with_fixtures('./eruditarticle/tests/fixtures/article/keywords', EruditArticle)
class TestGetKeywords:

    @with_value('1039501ar.xml', 'get_keywords')
    def test_can_return_keywords_of_tei_articles(self, value):
        assert tuple(value.keys()) == ('fr', 'en',)
        assert value['fr'] == ["Premières Nations", "enfants", "discrimination", "droits de la personne", ]  # noqa
        assert value['en'] == ["First Nations", "children", "discrimination", "human rights", ]

    @with_value('1043568ar.xml', 'get_keywords')
    def test_can_return_equivalent_keywords_in_the_lang_order_defined_in_the_article(self, value):  # noqa
        assert tuple(value.keys()) == ('fr', "en", "pt",)


@with_fixtures('./eruditarticle/tests/fixtures/article/section_titles', EruditArticle)
class TestSectionTitle(object):

    def test_can_return_section_titles(self):
        value = self.test_objects['1027883ar.xml'].get_section_titles(
            level=1
        )
        assert value == {
            'main': "Paroles et points de vue atikamekw nehirowisiwok",
            'paral': collections.OrderedDict(),
        }

        value = self.test_objects['1027883ar.xml'].get_section_titles(
            level=2
        )

        assert value == {
            'main': "Paroles d&#8217;a&#238;n&#233;s nehirowisiwok",
            'paral': collections.OrderedDict(),
        }

    def test_can_return_multilingual_section_titles(self):
        value = self.test_objects['1030384ar.xml'].get_section_titles(
            level=1
        )

        paral = collections.OrderedDict()
        paral['en'] = "Special Edition: Undertaking and innovating in a globalised economy..."
        paral['es'] = "Dossier especial: Emprender e innovar en una econom&#237;a globalizada&#8230;"  # noqa

        assert value == {
            'main': "Dossier sp&#233;cial&#160;: Entreprendre et innover dans une &#233;conomie globalis&#233;e...",  # noqa
            'paral': paral,
        }


@with_fixtures('./eruditarticle/tests/fixtures/article/notegen', EruditArticle)
class TestArticleNoteGen(object):

    @with_value('1006336ar.xml', 'get_notegens')
    def test_can_return_its_notegen(self, value):
        assert value == [{
            "type": "edito",
            "content": ["Une version ant&#233;rieure de ce texte &#224; &#233;t&#233; publi&#233;e dans <em>Le Devoir </em>du 7 mars 2011."]  # noqa
        }]

    @with_value('1006460ar.xml', 'get_notegens')
    def test_can_return_its_notegen_with_links(self, value):
        assert value == [{
            "type": "edito",
            "content": ['Pour obtenir la liste des sigles utilis&#233;s dans cet article et les r&#233;f&#233;rences compl&#232;tes aux oeuvres de Marie-Claire Blais, <a href="http://www.erudit.org/revue/vi/2011/v37/n1/1006456ar.html">voir p.&#160;7</a>.']  # noqa
        }]

    @with_value('1007816ar.xml', 'get_notegens')
    def test_can_return_its_notegen_with_biography(self, value):
        assert value == [{
            "type": "edito",
            "content": ["Sophie Th&#233;riault est professeure &#224; la Facult&#233; de droit de l&#8217;Universit&#233; d&#8217;Ottawa, Section de droit civil. Elle est &#233;galement membre du Barreau du Qu&#233;bec, du Centre du droit de l&#8217;environnement et de la durabilit&#233; mondiale de l&#8217;Universit&#233; d&#8217;Ottawa et du Centre de recherche et d&#8217;enseignement sur les droits de la personne de l&#8217;Universit&#233; d&#8217;Ottawa. David Robitaille est professeur &#224; la Facult&#233; de droit de l&#8217;Universit&#233; d&#8217;Ottawa, Section de droit civil. Il est &#233;galement membre du Barreau du Qu&#233;bec et du Centre de recherche et d&#8217;enseignement sur les droits de la personne de l&#8217;Universit&#233; d&#8217;Ottawa. Cet article a &#233;t&#233; r&#233;alis&#233; gr&#226;ce &#224; l&#8217;appui financier de la Fondation du Barreau du Qu&#233;bec, que nous remercions vivement. Nos remerciements vont &#233;galement &#224; nos assistants de recherche Camille Provencher, Pierre-Alexandre Henri, Nora Szeles et Karine H&#233;bert, ainsi qu&#8217;&#224; notre coll&#232;gue S&#233;bastien Grammond, pour ses commentaires judicieux."]  # noqa
        }, {
            "type": "edito",
            "content": [
                "Citation: (2011) 57:2 McGill LJ 211",
                "R&#233;f&#233;rence&#160;: (2011) 57&#160;:&#160;2 RD McGill 211",
            ]
        }]

    @with_value('1038621ar.xml', 'get_notegens')
    def test_can_return_its_notegen_with_multiple_paragraphs(self, value):
        assert value == [{
            "type": "edito",
            "content": ["Le pr&#233;sent texte suscite un questionnement approfondi sur l&#8217;&#233;conomie du contrat. Le lecteur trouvera des &#233;l&#233;ments de r&#233;ponse dans le texte suivant&#160;: &#171;&#160;L&#8217;apport &#233;pist&#233;mologique de la notion d&#8217;&#233;conomie du contrat en mati&#232;re d&#8217;interpr&#233;tation&#160;&#187;, (2016) 57:4 C&#160;de&#160;D &#224; para&#238;tre en d&#233;cembre."]  # noqa
        }, {
            "type": "auteur",
            "content": ["Je tiens &#224; remercier les professeurs Andr&#233; B&#233;langer (Universit&#233; Laval) et Martin Ndende (Universit&#233; de Nantes) sous la direction desquels s&#8217;effectue ma th&#232;se intitul&#233;e &#171;&#160;L&#8217;&#233;conomie du contrat dans l&#8217;effet obligatoire des clauses du contrat&#160;: l&#8217;exemple du contrat de transport&#160;&#187;."]  # noqa
        }]


@with_fixtures('./eruditarticle/tests/fixtures/article/savant/complet', EruditArticle)
class TestArticleSavantComplet(object):

    @with_value('1001948ar.xml', 'get_first_page')
    def test_can_return_its_first_page(self, value):
        assert value == '133'

    @with_value('1001948ar.xml', 'get_last_page')
    def test_can_return_its_last_page(self, value):
        assert value == "162"

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
        assert self.test_objects['1001948ar.xml'].get_html_title() == 'La pr&#233;cision des analystes financiers en Europe&#160;: l&#8217;effet pays et l&#8217;effet secteur revisit&#233;s'  # noqa
        assert self.test_objects['1001948ar_alt.xml'].get_html_title() == 'La pr&#233;cision des analystes financiers en Europe&#160;: l&#8217;effet pays et l&#8217;effet secteur <strong>test</strong> test 2  revisit&#233;s'   # noqa

    def test_publication_period(self):
        assert self.test_objects['1001948ar.xml'].get_publication_period() == 'Juin 2010'
        assert self.test_objects['009255ar.xml'].get_publication_period() ==\
            'November 2003, February 2004'
        assert self.test_objects['1005860ar.xml'].get_publication_period() == "2008–2009"

    def test_can_return_titles_subtitles(self):
        from eruditarticle.objects.base import Title

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
        EXPECTED = "Esth&#233;tique et s&#233;miotique :\xa0Pr&#233;sentation / Aesthetics and Semiotics : Presentation"  # noqa
        assert self.test_objects['1005860ar.xml'].get_formatted_html_title() == EXPECTED
        assert self.test_objects['1005860ar.xml'].get_title(formatted=True, html=True) == EXPECTED

        EXPECTED = '<em>Sociologie des relations professionnelles</em>, Par Michel Lallement, Nouvelle &#233;dition, Paris&#160;: La D&#233;couverte, collection Rep&#232;res, 2008, 121&#160;p., ISBN 978-2-7071-5446-0. / <em>Sociologie du travail&#160;: les relations professionnelles</em>, Par Antoine Bevort et Annette Jobert, Paris&#160;: Armand Collin, collection U, 2008, 268&#160;p., ISBN 978-2-200-34571-6.'  # noqa
        assert self.test_objects['044308ar.xml'].get_formatted_html_title() == EXPECTED
        assert self.test_objects['044308ar.xml'].get_title(formatted=True, html=True) == EXPECTED

    def test_can_return_journal_titles(self):
        from eruditarticle.objects.base import Title

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
        assert self.test_objects['044308ar.xml'].get_formatted_journal_title() == "Relations industrielles / Industrial Relations"  # noqa

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


@with_fixtures('./eruditarticle/tests/fixtures/article/savant/minimal', EruditArticle)
class TestArticleSavantMinimal(object):

    def test_can_return_titles_and_subtitles(self):
        from eruditarticle.objects.base import Title
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


@with_fixtures('./eruditarticle/tests/fixtures/article/format_person_name/', EruditArticle)
class TestFormatPersonName(object):

    @pytest.mark.parametrize('objectname,expected', [
        ('no_authors', ""),
        ('multiple_authors', "Marion Sauvaire et Érick Falardeau"),
        ('strip_tags', "Réjean Savard"),
        ('firstname_lastname', "Natascha Niederstrass"),
        ('with_othername', "Georges L. Bastin"),
        ('firstname_lastname_alias', "Patrick Straram, alias le Bison ravi"),
        ('only_alias', "Aude"),
        ('only_firstname', "Presseau"),
        ('only_lastname', "Marbic"),
        ('with_suffix', "Thibault Martin Ph.D."),
        ('with_guest_editor', "Justin K. Bisanswa"),
    ])
    @pytest.mark.parametrize('style', [None, 'invalid'])
    def test_get_formatted_authors(self, objectname, style, expected):
        obj = self.test_objects[objectname + '.xml']
        assert obj.get_authors(formatted=True, style=style) == expected

    @pytest.mark.parametrize('objectname,expected', [
        ('no_authors', ""),
        ('multiple_authors', "Sauvaire, M. & Falardeau, É."),
        ('strip_tags', "Savard, R."),
        ('firstname_lastname', "Niederstrass, N."),
        ('with_othername', "Bastin, G. L."),
        ('firstname_lastname_alias', "Straram, P."),
        ('only_alias', "Aude"),
        ('only_firstname', "Presseau"),
        ('only_lastname', "Marbic"),
        ('with_suffix', "Martin, T."),
        ('with_guest_editor', "Bisanswa, J. K."),
    ])
    def test_get_formatted_authors_apa(self, objectname, expected):
        obj = self.test_objects[objectname + '.xml']
        assert obj.get_authors(formatted=True, style='apa') == expected

    @pytest.mark.parametrize('objectname,expected', [
        ('no_authors', ""),
        ('multiple_authors', "Sauvaire, Marion et Érick Falardeau."),
        ('strip_tags', "Savard, Réjean."),
        ('firstname_lastname', "Niederstrass, Natascha."),
        ('with_othername', "Bastin, Georges L."),
        ('firstname_lastname_alias', "Straram, Patrick."),
        ('only_alias', "Aude."),
        ('only_firstname', "Presseau."),
        ('only_lastname', "Marbic."),
        ('with_suffix', "Martin, Thibault."),
        ('with_guest_editor', "Bisanswa, Justin K."),
    ])
    def test_get_formatted_authors_mla(self, objectname, expected):
        obj = self.test_objects[objectname + '.xml']
        assert obj.get_authors(formatted=True, style='mla') == expected

    @pytest.mark.parametrize('objectname,expected', [
        ('no_authors', ""),
        ('multiple_authors', "Sauvaire, Marion et Falardeau, Érick"),
        ('strip_tags', "Savard, Réjean"),
        ('firstname_lastname', "Niederstrass, Natascha"),
        ('with_othername', "Bastin, Georges L."),
        ('firstname_lastname_alias', "Straram, Patrick"),
        ('only_alias', "Aude"),
        ('only_firstname', "Presseau"),
        ('only_lastname', "Marbic"),
        ('with_suffix', "Martin, Thibault"),
        ('with_guest_editor', "Bisanswa, Justin K."),
    ])
    def test_get_formatted_authors_chicago(self, objectname, expected):
        obj = self.test_objects[objectname + '.xml']
        assert obj.get_authors(formatted=True, style='chicago') == expected


@with_fixtures('./eruditarticle/tests/fixtures/article/find_authors/', EruditArticle)
class TestFindAuthors(object):
    @with_value('with_translator_as_contributor.xml', 'get_authors')
    def test_can_exclude_translators(self, value):
        assert people_to_dict(value) == [
            {
                'affiliations': ['Universidade de São Paulo'],
                'email': None,
                'firstname': 'Ismail',
                'lastname': 'Xavier',
                'organization': None,
                'othername': None,
                'role': {},
                'suffix': None
            }
        ]


@with_fixtures('./eruditarticle/tests/fixtures/article/culturel/minimal', EruditArticle)
class TestArticleCulturelMinimal(object):

    def test_all_instances(self):
        for object_name, article in self.test_objects.items():
            assert isinstance(article, EruditArticle)

    def test_can_return_its_title(self):
        from eruditarticle.objects.base import Title
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

    @with_value('67660ac.xml', 'get_titles')
    def test_untitled_article_can_return_its_title(self, value):
        from eruditarticle.objects.base import Title
        assert value == {
            'main': Title(
                title=None,
                subtitle=None,
                lang='fr',
            ),
            'paral': [],
            'equivalent': [],
            'reviewed_works': []
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


@pytest.mark.parametrize('fixturename,isroc', [
    ('article/culturel/minimal/34598ac.xml', False),
    ('article/savant/minimal/602354ar.xml', True),
])
def test_article_is_of_type_roc(fixturename, isroc):
    path = './eruditarticle/tests/fixtures/{}'.format(fixturename)
    with open(path, 'rb') as fp:
        article = EruditArticle(fp.read())
    assert article.is_of_type_roc == isroc


def test_article_title_with_note():
    # An article title's note doesn't end up in the title, with or without markup.
    path = './eruditarticle/tests/fixtures/article/savant/minimal/602354ar.xml'
    with open(path, 'rb') as fp:
        article = EruditArticle(fp.read())
    title = article.find('grtitre/titre')
    renvoi_elem = E.renvoi("foobar", id='id1', idref='idref1', typeref='note')
    title.append(renvoi_elem)
    assert 'foobar' not in article.get_formatted_title()
    assert 'foobar' not in article.get_formatted_html_title()
