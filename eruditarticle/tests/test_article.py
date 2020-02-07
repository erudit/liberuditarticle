import collections
import pytest
from lxml.builder import E

from eruditarticle.objects import EruditArticle, Title
from eruditarticle.tests.decorators import with_value, with_fixtures


class Title(Title):
    def __init__(self, title=None, subtitle=None, lang=None):
        self.lang = lang
        self.title = title
        self.subtitle = subtitle


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
        assert value[0]['content'] == """<p class="alinea"><em>En fin de première année de formation à l’enseignement primaire, les étudiants du canton de Vaud en Suisse sont certifiés par des examens de différentes natures. Pour cette recherche à caractère exploratoire, nous avons retenu deux certifications particulières. La première concerne un module intitulé </em>Savoirs mathématiques et enseignement<em>, qui est certifié par un questionnaire à choix multiples (QCM) et qui exige des étudiants non seulement qu’ils répondent aux questions, mais également qu’ils indiquent leurs degrés de certitude des réponses données. Ce faisant, ils s’autoévaluent et cette estimation est prise en compte dans la réussite à l’examen. La seconde concerne un module intitulé </em>Enseignement et apprentissage<em>. L’examen se structure par des questions ouvertes testant les capacités d’analyse de tâches distribuées aux élèves des classes de la région. L’article présente les résultats d’une recherche visant à comprendre les liens entre des expériences évaluatives et des postures en formation de quatre étudiantes, puis à définir d’éventuelles logiques de formation. Nous avons relevé quatre postures qui remettent en question le rapport aux savoirs de la profession.</em></p>"""  # noqa

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

    @with_value('1043074ar.xml', 'get_abstracts', html=True)
    def test_can_convert_alinea_to_p(self, value):
        assert value[0]['content'] == """<p class="alinea">The aim of the paper is to track the scale and the strategy of European multinational firms related to the internationalization of their R&amp;D. We address two questions: 1. Can we confirm the general view assuming a growing trend in the internationalisation of technology? 2. Does the “home base augmenting” dominant strategy observed in the 1990s still hold? We use a patent data set for a sample of 349 firms and two time periods 1994-1996 and 2003-2005. We find out: 1) the remaining importance of the national technological bases of MNCs, 2) R&amp;D internationalisation is not continuously growing over the period under observation, 3) an emerging trend working to the detriment of the home base augmenting strategy.</p>"""  # noqa

    @with_value('602618ar.xml', 'get_abstracts', html=True)
    def test_can_convert_listeord_to_ol(self, value):
        assert value[0]['content'] == """<p class="alinea">Dans les subordonnées finales introduites par <em>damit</em>, on constate que le Präteritum allemand peut entrer en concurrence avec les formes subjonctives avec lesquelles il est alors commutable sans changement appréciable de sens :</p><ol class="lettremin" start="1"><li><p class="alinea">Ich weckte sie, wenn sie verschlief, <em>damit</em> sie rechtzeitig zur Kirche <em>kam</em>.</p><p class="alinea">Hauser-Suida, Hoppe-Beugel (1972:40)</p><p class="alinea">+ <em>damit</em> sie rechtzeitig zur Kirche <em>käme</em>.</p></li></ol><p class="alinea">mais que dans ce cas, l’alternance du Präteritum avec le Perfekt — autrement très fréquente — est interdite. Qu’il y ait des traits communs entre le Konjunktiv II et le Präteritum est un fait que signale la synapse totale de ces deux formes de la conjugaison régulière :</p><ol class="lettremin" start="2"><li><p class="alinea">Sie <em>fragte</em> ihn um Rat. (indicatif)</p></li><li><p class="alinea">Er wäre der letzte, den ich um Rat <em>fragte</em>.</p></li></ol><p class="alinea">et la synapse partielle des formes irrégulières (voir exemple (a)).</p><p class="alinea">Nous allons essayer de dégager les divers effets de sens qui découlent de l’emploi de l’une ou de l’autre forme dans la subordonnée finale introduite par <em>damit</em>, pour enfin réexaminer le signifié de puissance du Präteritum allemand, et proposer un lien avec le Konjunktiv II.</p>""" # noqa

    @with_value('1005712ar.xml', 'get_abstracts', html=True)
    def test_can_convert_listenonord_to_ul(self, value):
        assert value[0]['content'] == """<p class="alinea">Contrairement à d’autres crimes commis au sein du cercle familial, le crime passionnel, pourtant très visible socialement, n’a jamais fait l’objet d’une critique sociale ou psychologique efficace comme c’est le cas pour l’infanticide depuis longtemps déjà, ou plus récemment pour les abus sexuels ou le viol conjugal.</p><p class="alinea">Sur la base d’un corpus de 337 crimes et d’outils d’analyse variés, nous soulignerons trois aspects :</p><ul class="tiret"><li><p class="alinea">Dangerosité du milieu familial et conjugal, surtout pour les femmes.</p></li><li><p class="alinea">Déni de cette dangerosité dans le discours médiatique, voire psychiatrique.</p></li><li><p class="alinea">Dangerosité masquée enfin, car ces criminels, hommes et femmes, fonctionnent dans une pseudo-normalité.</p></li></ul>""" # noqa

    @with_value('1043218ar.xml', 'get_abstracts', html=True)
    def test_can_convert_bloccitation_to_blockquote(self, value):
        assert value[0]['content'] == """<p class="alinea">Lorsque le directeur de <em>La Revue musicale </em><em><span class="petitecap">sim</span></em>, Jules Écorcheville, part pour le front en 1914, il écrit à son ami Émile Vuillermoz :</p><blockquote class="bloccitation"><p class="alinea">Si je ne reviens pas, je vous recommande notre oeuvre, cher ami. Et surtout, si vous tenez à me faire plaisir dans l’autre monde, efforcez-vous de maintenir la concorde et l’harmonie entre les différents éléments qui vont se trouver en présence à ma disparition. Notre revue est faite de différentes pièces ajustées (Amis, <span class="petitecap">sim</span>, etc.), qui tiennent en équilibre par miracle, quelques années de cohésion sont absolument nécessaires encore et c’est précisément cette concentration de nos différentes forces qu’il faudrait maintenir. En tout cas, il ne faudrait pas que ma disparition entraînât celle d’une oeuvre qui nous a coûté, à tous, tant de peine. N’est-il pas vrai ?</p></blockquote><p class="alinea">Malgré le souhait d’Écorcheville, <em>La Revue </em><em><span class="petitecap">sim</span></em> disparaîtra, mais pas pour longtemps puisqu’elle donnera naissance à deux nouveaux organismes en 1917 et 1920. Pendant la guerre, les anciens de <em>La Revue </em><em><span class="petitecap">sim</span></em> dont Lionel de La Laurencie, vont créer la Société française de musicologie (<span class="petitecap">sfm</span>) sur les ruines de la Société internationale de musique et publieront un <em>Bulletin </em>qui deviendra la <em>Revue de musicologie. </em>Loin de l’actualité, s’écartant délibérément du contexte sociopolitique et culturel, la <span class="petitecap">sfm</span> et son <em>Bulletin </em>favoriseront une approche très « scientifique » et relativement nouvelle en France, de la musicologie, bien qu’encore teintée par les tendances historicisantes à la manière de la Schola Cantorum et écartant pour un temps toute la musicologie germanique. En parallèle, sous les auspices du musicologue Henry Prunières qui s’écarte résolument de la <span class="petitecap">sfm</span>, est créée <em>La Revue musicale</em>. C’est à partir d’un réseau international qui place la musicologie française au coeur de l’action musicale contemporaine que Prunières établit de nouvelles alliances avec le milieu des arts et de la littérature pour fonder l’une des plus célèbres revues musicales de la première moitié du <span class="petitecap">xx</span><sup>e</sup> siècle. À partir de documents inédits, nous étudierons les circonstances qui mènent à la refondation de <em>La Revue musicale</em> sur les cendres de la <em>Revue </em><em><span class="petitecap">sim</span></em> entre 1915 et 1919. Nous verrons ainsi comment les hasards de la guerre mènent Prunières à entreprendre la carrière d’éditeur et comment le musicologue conçoit le projet international de la revue dans un contexte de guerre qui contribue à une redéfinition des cultures nationales.</p><p class="alinea">Il est difficile d’extrapoler sur ce qu’aurait pu être l’avenir de <em>La Revue musicale </em><em><span class="petitecap">sim</span></em> si la guerre n’avait pas eu lieu. Il est par contre possible de documenter et de comprendre le rôle que la Grande Guerre jouera dans l’essor d’une nouvelle dynamique pour la musicologie française dont la division d’abord justifiée par le conflit aura des conséquences à long terme sur l’échiquier international de la discipline.</p>""" # noqa

    @with_value('1056320ar.xml', 'get_abstracts', html=True)
    def test_can_convert_renvoi_to_footnote_links(self, value):
        assert value[0]['content'] == """<p class="alinea"><em>Vu son expertise en classe et dans l’école, l’enseignant associé est considéré comme une personne essentielle à la formation initiale en enseignement. Des attentes à son égard sont formulées par les instances ministérielles (gouvernement du Québec, 2002, 2008), mais aussi par les stagiaires (Caron, Portelance &amp; Martineau, 2013). Pour répondre, l’enseignant associé est fortement incité à s’inscrire dans un processus de formation continue, ce qui lui permet d’enrichir ses pratiques de formateur du stagiaire. Dans le but de soutenir le développement des compétences attendues des enseignants associés (Portelance, Gervais, Lessard, Beaulieu et al, 2008), une recherche subventionnée par le ministère de l’Éducation du Québec</em><a href="#no1" id="re1no1" class="norenvoi">[1]</a><em> utilise une approche collaborative avec une communauté de pratique composée d’enseignants associés. Les membres sont engagés dans une démarche de réflexion et de coconstruction de sens (Bourassa, Philion &amp; Chevalier, 2007). Les discussions portent sur les pratiques d’encadrement du stagiaire. L’analyse de leurs propos met en évidence les manifestations de la dynamique interactionnelle qui favorise leur codéveloppement professionnel.</em></p>"""  # noqa

    @with_value('1057080ar.xml', 'get_abstracts', html=True)
    def test_can_convert_renvoi_to_footnote_links_in_title(self, value):
        assert value[0]['title'] == 'Résumé <a href="#no1" id="re1no1" class="norenvoi">[1]</a>'  # noqa

    @with_value('1056946ar.xml', 'get_abstracts', html=True)
    def test_can_convert_indice_tag_to_sub_tag(self, value):
        assert value[0]['content'] == """<p class="alinea">Après avoir rappelé les contextes théorique et économique dans lequel s’inscrit cet article, nous présentons un premier modèle économétrique existant d’élasticité-prix. Puis, nous introduisons un modèle micro-économique dynamique en partant de l’exemple concret d’une compagnie d’assurance non-vie qui souhaite changer de stratégie de renouvellement. Nous étudions les effets de son choix de prix (primes) sur son portefeuille et son chiffre d’affaires, dans un contexte de concurrence. La variation du nombre de contrats en portefeuille et du chiffre d’affaires de la compagnie entre deux instants t<sub>0</sub> et t<sub>1</sub> est déterminée. Une application numérique sur trois branches d’assurance d’entreprises précède la conclusion.</p>"""  # noqa


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

    @with_value('1043568ar.xml', 'get_keywords')
    def test_can_remove_tags_in_keywords(self, value):  # noqa
        assert value['fr'] == ['formation à l’enseignement', 'postures en formation',
                               'rapport à l’évaluation', 'rapport au savoir']

    @with_value('1043568ar.xml', 'get_keywords', html=True)
    def test_can_convert_marquage_in_keywords(self, value):  # noqa
        assert value['fr'] == ['formation à l’enseignement',
                               '<span class=""><em>postures en formation</em></span>',
                               'rapport à l’évaluation', 'rapport au savoir']


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
            'main': "Paroles d’aînés nehirowisiwok",
            'paral': collections.OrderedDict(),
        }

    def test_can_return_multilingual_section_titles(self):
        value = self.test_objects['1030384ar.xml'].get_section_titles(
            level=1
        )

        paral = collections.OrderedDict()
        paral['en'] = "Special Edition: Undertaking and innovating in a globalised economy..."
        paral['es'] = "Dossier especial: Emprender e innovar en una economía globalizada…"  # noqa

        assert value == {
            'main': "Dossier spécial : Entreprendre et innover dans une économie globalisée...",  # noqa
            'paral': paral,
        }


@with_fixtures('./eruditarticle/tests/fixtures/article/notegen', EruditArticle)
class TestArticleNoteGen(object):

    @with_value('1006336ar.xml', 'get_notegens')
    def test_can_return_its_notegen(self, value):
        assert value == [{
            "type": "edito",
            "scope": "numero",
            "content": ["Une version antérieure de ce texte à été publiée dans <em>Le Devoir </em>du 7 mars 2011."]  # noqa
        }]

    @with_value('1006460ar.xml', 'get_notegens')
    def test_can_return_its_notegen_with_links(self, value):
        assert value == [{
            "type": "edito",
            "scope": "numero",
            "content": ['Pour obtenir la liste des sigles utilisés dans cet article et les références complètes aux oeuvres de Marie-Claire Blais, <a href="http://www.erudit.org/revue/vi/2011/v37/n1/1006456ar.html">voir p. 7</a>.']  # noqa
        }]

    @with_value('1007816ar.xml', 'get_notegens')
    def test_can_return_its_notegen_with_biography(self, value):
        assert value == [{
            "type": "edito",
            "scope": "numero",
            "content": ["Sophie Thériault est professeure à la Faculté de droit de l’Université d’Ottawa, Section de droit civil. Elle est également membre du Barreau du Québec, du Centre du droit de l’environnement et de la durabilité mondiale de l’Université d’Ottawa et du Centre de recherche et d’enseignement sur les droits de la personne de l’Université d’Ottawa. David Robitaille est professeur à la Faculté de droit de l’Université d’Ottawa, Section de droit civil. Il est également membre du Barreau du Québec et du Centre de recherche et d’enseignement sur les droits de la personne de l’Université d’Ottawa. Cet article a été réalisé grâce à l’appui financier de la Fondation du Barreau du Québec, que nous remercions vivement. Nos remerciements vont également à nos assistants de recherche Camille Provencher, Pierre-Alexandre Henri, Nora Szeles et Karine Hébert, ainsi qu’à notre collègue Sébastien Grammond, pour ses commentaires judicieux."]  # noqa
        }, {
            "type": "edito",
            "scope": "numero",
            "content": [
                "Citation: (2011) 57:2 McGill LJ 211",
                "Référence : (2011) 57 : 2 RD McGill 211",
            ]
        }]

    @with_value('1038621ar.xml', 'get_notegens')
    def test_can_return_its_notegen_with_multiple_paragraphs(self, value):
        assert value == [{
            "type": "edito",
            "scope": "numero",
            "content": ["Le présent texte suscite un questionnement approfondi sur l’économie du contrat. Le lecteur trouvera des éléments de réponse dans le texte suivant : « L’apport épistémologique de la notion d’économie du contrat en matière d’interprétation », (2016) 57:4 C de D à paraître en décembre."]  # noqa
        }, {
            "type": "auteur",
            "scope": None,
            "content": ["Je tiens à remercier les professeurs André Bélanger (Université Laval) et Martin Ndende (Université de Nantes) sous la direction desquels s’effectue ma thèse intitulée « L’économie du contrat dans l’effet obligatoire des clauses du contrat : l’exemple du contrat de transport »."]  # noqa
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
        assert self.test_objects['1001948ar.xml'].get_html_title() == 'La précision des analystes financiers en Europe : l’effet pays et l’effet secteur revisités'  # noqa
        assert self.test_objects['1001948ar_alt.xml'].get_html_title() == 'La précision des analystes financiers en Europe : l’effet pays et l’effet secteur <strong>test</strong> test 2 revisités'   # noqa
        # Check that <liensimple> tags are not stripped or displayed as links. They should be
        # displayed as text.
        assert self.test_objects['007801ar.xml'].get_html_title() == 'Sites Internet des Archives nationales du Canada et des Archives nationales du Québec &lt;http://www.archives.ca&gt; et &lt;http://www.anq.gouv.qc.ca&gt;. Sites évalués à la fin mars 2003.'  # noqa

    def test_publication_period(self):
        assert self.test_objects['1001948ar.xml'].get_publication_period() == 'Juin 2010'
        assert self.test_objects['009255ar.xml'].get_publication_period() ==\
            'November 2003, February 2004'
        assert self.test_objects['1005860ar.xml'].get_publication_period() == "2008–2009"

    def test_can_return_titles_subtitles(self):
        assert self.test_objects['1005860ar.xml'].get_titles() == {
            'main': Title(title="Esthétique et sémiotique", subtitle="Présentation", lang="fr"),  # noqa
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
                    '<em>Sociologie des relations professionnelles</em>, Par Michel Lallement, Nouvelle édition, Paris : La Découverte, collection Repères, 2008, 121 p., ISBN 978-2-7071-5446-0.',  # noqa
                    '<em>Sociologie du travail : les relations professionnelles</em>, Par Antoine Bevort et Annette Jobert, Paris : Armand Collin, collection U, 2008, 268 p., ISBN 978-2-200-34571-6.'  # noqa
            ]
        }

        assert self.test_objects['1004725ar.xml'].get_titles() == {
            'main': Title(title="Introduction: Food, Language, and Identity", subtitle=None, lang="en"),  # noqa
            'paral': [],
            'equivalent': [Title(title="Cuisine, langue et identité", subtitle=None, lang="fr")],  # noqa
            'reviewed_works': [],
        }

        assert self.test_objects['1003507ar.xml'].get_titles() == {
            'main': Title(title="Reconceptualizing Translation – Some Chinese Endeavours", subtitle=None, lang="en"),  # noqa
            'paral': [],
            'equivalent': [],
            'reviewed_works': [],
        }

        assert self.test_objects['1006389ar.xml'].get_titles() == {
            'main': Title(title=None, subtitle=None, lang="fr"),  # noqa
            'paral': [],
            'equivalent': [],
            'reviewed_works': [
                'C<span class="petitecap">oulombe</span> Maxime, 2010, <em>Le monde sans fin des jeux vidéo</em>. Paris, Presses universitaires de France, coll. La nature humaine, 160 p., bibliogr.'  # noqa
            ],
        }

        assert self.test_objects['1056361ar.xml'].get_titles() == {
            'main': Title(
                title='UN ROMAN « NÉ DANS SA PROPRE NÉGATION »',
                subtitle='L’articulation du littéraire et du religieux dans <em>Angéline</em> <em>de</em> <em>Montbrun</em> de Laure Conan',  # noqa
                lang='fr',
            ),
            'paral': [],
            'equivalent': [
                Title(
                    title='A NOVEL “BORN IN ITS OWN NEGATION”',
                    subtitle='THE ARTICULATION OF THE LITERARY AND THE RELIGIOUS IN LAURE CONAN’S <em>ANGÉLINE DE MONTBRUN</em>',  # noqa
                    lang='en',
                ),
                Title(
                    title='UNA NOVELA “NACIDA EN SU PROPIA NEGACIÓN”',
                    subtitle='LA ARTICULACIÓN DE LO LITERARIO Y LO RELIGIOSO EN <em>ANGÉLINE DE MONTBRUN</em>, DE LAURE CONAN',  # noqa
                    lang='es',
                ),
            ],
            'reviewed_works': [],
        }

        assert self.test_objects['1042058ar.xml'].get_titles() == {
            'main': Title(title=None, subtitle=None, lang='fr'),
            'paral': [],
            'equivalent': [],
            'reviewed_works': [],
        }

        assert self.test_objects['1043053ar.xml'].get_titles() == {
            'main': Title(
                title="L'impossible vérité de l'histoire des pensionnats",
                subtitle='Traumatismes, victimisation et réconciliation prématurée',
                lang='fr',
            ),
            'paral': [],
            'equivalent': [],
            'reviewed_works': [
                'C<span class="petitecap">ommission de vérité et réconciliation</span>, 2015, <em>Rapport final de la Commission de vérité et réconciliation du Canada</em>, Volume 1. <em>Pensionnats du Canada</em><em> :</em><em> L’histoire</em>, partie 1,<em> des origines à 1939</em>, 1072 p.',  # noqa
                'C<span class="petitecap">ommission de vérité et réconciliation</span>, 2015, Volume 1. <em>Pensionnats du Canada</em><em> :</em><em> L’histoire</em>, partie 2,<em> de 1939 à 2000</em>, 896 p.',  # noqa
                'C<span class="petitecap">ommission de vérité et réconciliation</span>, 2016, Volume 2. <em>Pensionnats du Canada</em><em> :</em><em> L’expérience inuite et nordique</em>, 290 p.',  # noqa
                'C<span class="petitecap">ommission de vérité et réconciliation</span>, 2015, Volume 3. <em>Pensionnats du Canada</em><em> :</em><em> L’expérience métisse</em>, 96 p.',  # noqa
                'C<span class="petitecap">ommission de vérité et réconciliation</span>, 2015, Volume 4. <em>Pensionnats du Canada</em><em> :</em><em> Enfants disparus et lieux de sépulture non marqués</em>, 304 p.',  # noqa
                'C<span class="petitecap">ommission de vérité et réconciliation</span>, 2016, Volume 5. <em>Pensionnats du Canada</em><em> :</em><em> Les séquelles</em>, 464 p.',  # noqa
                'C<span class="petitecap">ommission de vérité et réconciliation</span>, 2016, Volume 6. <em>Pensionnats du Canada</em><em> :</em><em> La réconciliation</em>, 352 p.',  # noqa
                'G<span class="petitecap">oulet</span> H., 2016, <em>Histoire des pensionnats indiens catholiques du Québec. Le rôle déterminant des pères oblats</em>. Montréal, Presses de l’Université de Montréal, 222 p.',  # noqa
                'N<span class="petitecap">iezen</span> R., 2013, <em>Truth and Indignation. Canada’s Truth and Reconciliation Commission on Indian Residential Schools</em>. Toronto, University of Toronto Press, 192 p.',  # noqa
            ],
        }

    def test_can_return_formatted_titles(self):
        EXPECTED = "Esthétique et sémiotique\xa0: présentation / Aesthetics and Semiotics: Presentation"  # noqa
        assert self.test_objects['1005860ar.xml'].get_formatted_html_title() == EXPECTED
        assert self.test_objects['1005860ar.xml'].get_title(formatted=True, html=True) == EXPECTED

        EXPECTED = '<em>Sociologie des relations professionnelles</em>, Par Michel Lallement, Nouvelle édition, Paris : La Découverte, collection Repères, 2008, 121 p., ISBN 978-2-7071-5446-0. / <em>Sociologie du travail : les relations professionnelles</em>, Par Antoine Bevort et Annette Jobert, Paris : Armand Collin, collection U, 2008, 268 p., ISBN 978-2-200-34571-6.'  # noqa
        assert self.test_objects['044308ar.xml'].get_formatted_html_title() == EXPECTED
        assert self.test_objects['044308ar.xml'].get_title(formatted=True, html=True) == EXPECTED

        EXPECTED = 'Colloque d’histoire antillaise : <span class="majuscule">C</span>ENTRE D’ENSEIGNEMENT SUPÉRIEUR LITTÉRAIRE DE POINTE-À-PITRE (25-28 avril 1969)'  # noqa
        assert self.test_objects['1056263ar.xml'].get_formatted_html_title() == EXPECTED
        assert self.test_objects['1056263ar.xml'].get_title(formatted=True, html=True) == EXPECTED

        EXPECTED = '<em>C’est fou la vie, pourquoi en faire une maladie?</em> Genèse et perspectives d’avenir du Mouvement Jeunes et santé mentale'  # noqa
        assert self.test_objects['1067047ar.xml'].get_formatted_html_title() == EXPECTED
        assert self.test_objects['1067047ar.xml'].get_title(formatted=True, html=True) == EXPECTED

    def test_can_return_journal_titles(self):
        assert self.test_objects['1006389ar.xml'].get_journal_titles() == {
            "main": Title(title="Anthropologie et Sociétés", subtitle=None, lang="fr"),
            "paral": [],
            "equivalent": [],
        }

        assert self.test_objects['1005860ar.xml'].get_journal_titles() == {
            "main": Title(title="Recherches sémiotiques", subtitle=None, lang="fr"),
            "paral": [Title(title="Semiotic Inquiry", subtitle=None, lang="en")],
            "equivalent": [],
        }

        assert self.test_objects['044308ar.xml'].get_journal_titles() == {
            "main": Title(title="Relations industrielles", subtitle=None, lang="fr"),
            "paral": [],
            "equivalent": [Title(title="Industrial Relations", subtitle=None, lang="en")],
        }

    def test_can_return_its_formatted_journal_title(self):
        assert self.test_objects['1005860ar.xml'].get_formatted_journal_title() == "Recherches sémiotiques / Semiotic Inquiry"  # noqa
        assert self.test_objects['044308ar.xml'].get_formatted_journal_title() == "Relations industrielles / Industrial Relations"  # noqa

    def test_can_return_languages(self):
        assert self.test_objects['1005860ar.xml'].get_languages() == ['fr', 'en']

    def test_can_return_references(self):
        references = self.test_objects['009255ar.xml'].get_references(html=False)
        assert references[0] == {'title': "Akenside, Mark. Poems. London: J. Dodsley, 1772.", 'doi': None}  # noqa
        assert len(references) == 53

        references = self.test_objects['1003507ar.xml'].get_references(html=False)
        assert references[3] == {'title': "Cheung, Martha P. Y. (2005): ‘To translate’ means ‘to exchange’? A new interpretation of the earliest Chinese attempts to define translation (‘fanyi’). Target. 17(1):27-48.", 'doi': '10.1075/target.17.1.03che'}  # noqa

    def test_can_return_references_with_markup(self):
        references = self.test_objects['009255ar.xml'].get_references()
        assert references[0] == {'title': "Akenside, Mark. <em>Poems</em>. London: J. Dodsley, 1772.", 'doi': None}  # noqa
        assert len(references) == 53

    def test_html_body(self):
        html = self.test_objects['1001948ar.xml'].get_html_body()
        assert 'Ferreira' in html

    def test_html_body_with_empty_alinea(self):
        html = self.test_objects['005722ar.xml'].get_html_body()
        assert 'The appearance of nature and landscape descriptions' in html
        html = self.test_objects['044581ar.xml'].get_html_body()
        assert 'L’historien Pierre Gaxotte pensa proposer la candidature d’Anouilh' in html

    def test_breaking_spaces_are_not_stripped_from_html_body(self):
        html = self.test_objects['1065852ar.xml'].get_html_body()
        assert 'Erratum\xa0: Une erreur s’est glissée dans le volume 52.1 de ' \
               '<em>Criminologie</em>. Dans le texte «\xa0Szabo, ou la volonté d’exister\xa0», ' \
               'de François Fenchel, nous aurions dû lire, à la page 8\xa0: «\xa0…il y a dans la ' \
               'reconnaissance de l’oeuvre celle de sa propre vie, de la valeur du chemin qu’il ' \
               'a tracé pour lui-même. La vie de Denis Szabo est une injonction à voir grand, ne ' \
               'fût-ce que dans l’espoir d’éviter un destin joué d’avance.\xa0» Nous vous prions ' \
               'de bien vouloir nous excuser pour cette erreur.' == html

    def test_get_formatted_title(self):
        # There should not be a capital letter after a colon.
        assert self.test_objects['1056361ar.xml'].get_formatted_title() == 'UN ROMAN « NÉ DANS SA PROPRE NÉGATION » : l’articulation du littéraire et du religieux dans Angéline de Montbrun de Laure Conan'  # noqa
        # There should be a capital letter after a colon if it was forced in the XML.
        assert self.test_objects['1056263ar.xml'].get_formatted_title() == 'Colloque d’histoire antillaise : CENTRE D’ENSEIGNEMENT SUPÉRIEUR LITTÉRAIRE DE POINTE-À-PITRE (25-28 avril 1969)'  # noqa


@with_fixtures('./eruditarticle/tests/fixtures/article/savant/minimal', EruditArticle)
class TestArticleSavantMinimal(object):

    def test_can_return_titles_and_subtitles(self):
        assert self.test_objects['602354ar.xml'].get_titles(html=False) == {
            'main': Title(title='Immigration, langues et performance économique : le Québec et l’Ontario entre 1970 et 1995', lang="fr", subtitle=None),  # noqa
            'equivalent': [
                Title(title='Immigration, Languages and Economic Performance: Quebec and Ontario between 1970 and 1995', lang='en', subtitle=None)  # noqa
            ],
            'paral': [],
            'reviewed_works': [],
        }

    def test_can_return_titles_with_malformed_grtitre(self):
        assert self.test_objects['001296ar.xml'].get_formatted_title() is not None

    def test_get_formatted_title(self):
        # There should not be a colon after a punctuation.
        assert self.test_objects['1054095ar.xml'].get_formatted_title() == 'Un français de référence acadien en émergence ? Étude sur les représentations métalexicographiques contemporaines de particularismes acadiens'  # noqa
        assert self.test_objects['004812ar.xml'].get_formatted_title() == 'The Tardy, Tasty and Chilly Thermophiles of the Champlain Sea'  # noqa

    def test_get_formatted_journal_title(self):
        # Check that get_formatted_journal_title() does not crash when there's an empty subtitle.
        assert self.test_objects['301900ar.xml'].get_formatted_journal_title() == "Revue d'histoire de l'Amérique française"  # noqa

    def test_get_title(self):
        assert self.test_objects['1055849ar.xml'].get_title(formatted=True, html=True) == 'The Resonance of Debussy for United States Post-Modernists'  # noqa

    def test_droitsauteur(self):
        assert self.test_objects['1039242ar.xml'].get_droitsauteur() == [
            {
                'text': "Droits d'auteur © Claire Peltier, 2017",
            }, {
                'href': 'http://creativecommons.org/licences/by/4.0/deed.fr',
                'img': 'http://licensebuttons.net/l/by/4.0/88x31.png',
            },
        ]

    def test_droitsauteur_with_empty_copyrights(self):
        assert self.test_objects['001118ar.xml'].get_droitsauteur() == []

    def test_get_doi_with_no_doi(self):
        assert self.test_objects['1042919ar.xml'].get_doi() is None


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
        ('with_suffix', "Thibault Martin, Ph.D."),
        ('with_guest_editor', "Justin K. Bisanswa"),
    ])
    @pytest.mark.parametrize('style', [None, 'invalid'])
    def test_get_formatted_authors(self, objectname, style, expected):
        obj = self.test_objects[objectname + '.xml']
        assert obj.get_authors(formatted=True, style=style) == expected

    def test_get_formatted_authors_with_and_without_suffixes(self):
        obj = self.test_objects['with_suffix.xml']
        assert obj.get_authors(formatted=True) == 'Thibault Martin, Ph.D.'
        assert obj.get_authors(formatted=True, suffixes=False) == 'Thibault Martin'

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
        ('white_space_before_firstname', "Connor, J. J."),
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
        assert self.test_objects['49222ac.xml'].get_titles(html=False) == {
            'main': Title(
                title='Love and death on long island',
                subtitle='Premier délice',
                lang='fr',
            ),
            'paral': [],
            'equivalent': [],
            'reviewed_works': ["Love and Death on Long Island (Rendez-vous à Long Island), Grande-Bretagne / Canada, 1997, 93 minutes"]  # noqa
        }

        assert self.test_objects['89930ac.xml'].get_titles(html=False) == {
            'main': Title(
                title='With Open Eyes: Affective Translation in Contemporary Art',
                subtitle=None,
                lang='en',
            ),
            'paral': [
                Title(
                    title='Les yeux grands ouverts : la traduction affective dans l’art contemporain',  # noqa
                    subtitle=None,
                    lang='fr',
                ),
            ],
            'equivalent': [],
            'reviewed_works': [],
        }

    def test_can_return_its_formatted_title(self):
        assert self.test_objects['90859ac.xml'].get_title(formatted=True, html=True) == 'Doubles vies : écris-moi des mots qui sonnent, sonnent, sonnent'  # noqa
        assert self.test_objects['90873ac.xml'].get_title(formatted=True, html=True) == 'God exists, Her Name Is Petrunya : à la fin, c’est l’eau qui gagne'  # noqa

    @with_value('67660ac.xml', 'get_titles')
    def test_untitled_article_can_return_its_title(self, value):
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
        assert self.test_objects['49222ac.xml'].get_reviewed_works(html=False) == ["Love and Death on Long Island (Rendez-vous à Long Island), Grande-Bretagne / Canada, 1997, 93 minutes"]  # noqa

    def test_get_doi_with_extra_space(self):
        assert self.test_objects['1009368ar.xml'].get_doi() == '10.7202/1009368ar'


def get_article(fixturename):
    path = './eruditarticle/tests/fixtures/{}'.format(fixturename)
    with open(path, 'rb') as fp:
        return EruditArticle(fp.read())


@pytest.mark.parametrize('fixturename,isroc', [
    ('article/culturel/minimal/34598ac.xml', False),
    ('article/savant/minimal/602354ar.xml', True),
])
def test_article_is_of_type_roc(fixturename, isroc):
    article = get_article(fixturename)
    assert article.is_of_type_roc == isroc


def test_article_title_with_note():
    # An article title's note doesn't end up in the title, with or without markup.
    article = get_article('article/savant/minimal/602354ar.xml')
    title = article.find('grtitre/titre')
    renvoi_elem = E.renvoi("foobar", id='id1', idref='idref1', typeref='note')
    title.append(renvoi_elem)
    assert 'foobar' not in article.get_formatted_title()
    assert 'foobar' not in article.get_formatted_html_title()


@pytest.mark.parametrize('html', [True, False])
def test_article_title_with_empty_alinea(html):
    # an empty <alinea/> element doesn't make us crash.
    article = get_article('article/savant/minimal/602354ar.xml')
    resume = article.find('resume')
    resume.append(E.alinea())
    article.get_abstracts(html=html)  # no crash


def test_stringified_elements_normalize_whitespaces():
    article = get_article('article/savant/minimal/602354ar.xml')
    title = article.find('grtitre/titre')
    title.text = 'foo\nbar'
    assert article.get_formatted_title() == 'foo bar'
    assert article.get_formatted_html_title() == 'foo bar'
