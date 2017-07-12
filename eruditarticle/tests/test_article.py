import collections
from eruditarticle.objects import EruditArticle
from eruditarticle.tests.decorators import with_value, with_fixtures


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


@with_fixtures('./eruditarticle/tests/fixtures/article/format_person_name/', EruditArticle)
class TestFormatPersonName(object):

    @with_value('strip_tags.xml', 'get_formatted_authors')
    def test_can_strip_elements_from_author_name(self, value):
        assert value == ['Réjean Savard']

    @with_value('firstname_lastname.xml', 'get_formatted_authors')
    def test_can_format_a_firstname_lastname(self, value):
        assert value == ['Natascha Niederstrass']

    @with_value('with_othername.xml', 'get_formatted_authors')
    def test_can_format_firstname_othername_lastname(self, value):
        assert value == ['Georges L. Bastin']

    @with_value('firstname_lastname_alias.xml', 'get_formatted_authors')
    def test_can_format_firstname_lastname_and_alias(self, value):
        assert value == ['Patrick Straram, alias le Bison ravi']

    @with_value('only_alias.xml', 'get_formatted_authors')
    def test_can_format_only_alias(self, value):
        assert value == ['Aude']

    @with_value('only_firstname.xml', 'get_formatted_authors')
    def test_can_format_only_firstname(self, value):
        assert value == ['Presseau']

    @with_value('only_lastname.xml', 'get_formatted_authors')
    def test_can_format_only_lastname(self, value):
        assert value == ['Marbic']

    @with_value('with_suffix.xml', 'get_formatted_authors')
    def test_can_format_name_with_suffix(self, value):
        assert value == ['Thibault Martin Ph.D.']


@with_fixtures('./eruditarticle/tests/fixtures/article/find_authors/', EruditArticle)
class TestFindAuthors(object):
    @with_value('with_translator_as_contributor.xml', 'get_authors')
    def test_can_exclude_translators(self, value):
        assert value == [
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

    @with_value('67660ac.xml', 'get_titles')
    def test_untitled_article_can_return_its_title(self, value):
        from eruditarticle.base import Title
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
