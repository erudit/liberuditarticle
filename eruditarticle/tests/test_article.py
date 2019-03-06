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
        assert value[0]['content'] == """<p class="alinea"><em>En fin de premi&#232;re ann&#233;e de formation &#224; l&#8217;enseignement primaire, les &#233;tudiants du canton de Vaud en Suisse sont certifi&#233;s par des examens de diff&#233;rentes natures. Pour cette recherche &#224; caract&#232;re exploratoire, nous avons retenu deux certifications particuli&#232;res. La premi&#232;re concerne un module intitul&#233; </em>Savoirs math&#233;matiques et enseignement<em>, qui est certifi&#233; par un questionnaire &#224; choix multiples (QCM) et qui exige des &#233;tudiants non seulement qu&#8217;ils r&#233;pondent aux questions, mais &#233;galement qu&#8217;ils indiquent leurs degr&#233;s de certitude des r&#233;ponses donn&#233;es. Ce faisant, ils s&#8217;auto&#233;valuent et cette estimation est prise en compte dans la r&#233;ussite &#224; l&#8217;examen. La seconde concerne un module intitul&#233; </em>Enseignement et apprentissage<em>. L&#8217;examen se structure par des questions ouvertes testant les capacit&#233;s d&#8217;analyse de t&#226;ches distribu&#233;es aux &#233;l&#232;ves des classes de la r&#233;gion. L&#8217;article pr&#233;sente les r&#233;sultats d&#8217;une recherche visant &#224; comprendre les liens entre des exp&#233;riences &#233;valuatives et des postures en formation de quatre &#233;tudiantes, puis &#224; d&#233;finir d&#8217;&#233;ventuelles logiques de formation. Nous avons relev&#233; quatre postures qui remettent en question le rapport aux savoirs de la profession.</em></p>"""  # noqa

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
        assert value[0]['content'] == """<p class="alinea">The aim of the paper is to track the scale and the strategy of European multinational firms related to the internationalization of their R&amp;D. We address two questions: 1. Can we confirm the general view assuming a growing trend in the internationalisation of technology? 2. Does the &#8220;home base augmenting&#8221; dominant strategy observed in the 1990s still hold? We use a patent data set for a sample of 349 firms and two time periods 1994-1996 and 2003-2005. We find out: 1) the remaining importance of the national technological bases of MNCs, 2) R&amp;D internationalisation is not continuously growing over the period under observation, 3) an emerging trend working to the detriment of the home base augmenting strategy.</p>"""  # noqa

    @with_value('602618ar.xml', 'get_abstracts', html=True)
    def test_can_convert_listeord_to_ol(self, value):
        assert value[0]['content'] == """<p class="alinea">Dans les subordonn&#233;es finales introduites par <em>damit</em>, on constate que le Pr&#228;teritum allemand peut entrer en concurrence avec les formes subjonctives avec lesquelles il est alors commutable sans changement appr&#233;ciable de sens&#160;:</p><ol class="lettremin" start="1"><li><p class="alinea">Ich weckte sie, wenn sie verschlief, <em>damit</em> sie rechtzeitig zur Kirche <em>kam</em>.</p><p class="alinea">Hauser-Suida, Hoppe-Beugel (1972:40)</p><p class="alinea">+&#160;<em>damit</em> sie rechtzeitig zur Kirche <em>k&#228;me</em>.</p></li></ol><p class="alinea">mais que dans ce cas, l&#8217;alternance du Pr&#228;teritum avec le Perfekt&#160;&#8212; autrement tr&#232;s fr&#233;quente&#160;&#8212; est interdite. Qu&#8217;il y ait des traits communs entre le Konjunktiv&#160;II et le Pr&#228;teritum est un fait que signale la synapse totale de ces deux formes de la conjugaison r&#233;guli&#232;re&#160;:</p><ol class="lettremin" start="2"><li><p class="alinea">Sie <em>fragte</em> ihn um Rat. (indicatif)</p></li><li><p class="alinea">Er w&#228;re der letzte, den ich um Rat <em>fragte</em>.</p></li></ol><p class="alinea">et la synapse partielle des formes irr&#233;guli&#232;res (voir exemple (a)).</p><p class="alinea">Nous allons essayer de d&#233;gager les divers effets de sens qui d&#233;coulent de l&#8217;emploi de l&#8217;une ou de l&#8217;autre forme dans la subordonn&#233;e finale introduite par <em>damit</em>, pour enfin r&#233;examiner le signifi&#233; de puissance du Pr&#228;teritum allemand, et proposer un lien avec le Konjunktiv&#160;II.</p>""" # noqa

    @with_value('1005712ar.xml', 'get_abstracts', html=True)
    def test_can_convert_listenonord_to_ul(self, value):
        assert value[0]['content'] == """<p class="alinea">Contrairement &#224; d&#8217;autres crimes commis au sein du cercle familial, le crime passionnel, pourtant tr&#232;s visible socialement, n&#8217;a jamais fait l&#8217;objet d&#8217;une critique sociale ou psychologique efficace comme c&#8217;est le cas pour l&#8217;infanticide depuis longtemps d&#233;j&#224;, ou plus r&#233;cemment pour les abus sexuels ou le viol conjugal.</p><p class="alinea">Sur la base d&#8217;un corpus de 337 crimes et d&#8217;outils d&#8217;analyse vari&#233;s, nous soulignerons trois aspects&#160;:</p><ul class="tiret"><li><p class="alinea">Dangerosit&#233; du milieu familial et conjugal, surtout pour les femmes.</p></li><li><p class="alinea">D&#233;ni de cette dangerosit&#233; dans le discours m&#233;diatique, voire psychiatrique.</p></li><li><p class="alinea">Dangerosit&#233; masqu&#233;e enfin, car ces criminels, hommes et femmes, fonctionnent dans une pseudo-normalit&#233;.</p></li></ul>""" # noqa

    @with_value('1043218ar.xml', 'get_abstracts', html=True)
    def test_can_convert_bloccitation_to_blockquote(self, value):
        assert value[0]['content'] == """<p class="alinea">Lorsque le directeur de <em>La Revue musicale </em><em><span class="petitecap">sim</span></em>, Jules &#201;corcheville, part pour le front en 1914, il &#233;crit &#224; son ami &#201;mile Vuillermoz&#160;:</p><blockquote class="bloccitation"><p class="alinea">Si je ne reviens pas, je vous recommande notre oeuvre, cher ami. Et surtout, si vous tenez &#224; me faire plaisir dans l&#8217;autre monde, efforcez-vous de maintenir la concorde et l&#8217;harmonie entre les diff&#233;rents &#233;l&#233;ments qui vont se trouver en pr&#233;sence &#224; ma disparition. Notre revue est faite de diff&#233;rentes pi&#232;ces ajust&#233;es (Amis, <span class="petitecap">sim</span>, etc.), qui tiennent en &#233;quilibre par miracle, quelques ann&#233;es de coh&#233;sion sont absolument n&#233;cessaires encore et c&#8217;est pr&#233;cis&#233;ment cette concentration de nos diff&#233;rentes forces qu&#8217;il faudrait maintenir. En tout cas, il ne faudrait pas que ma disparition entra&#238;n&#226;t celle d&#8217;une oeuvre qui nous a co&#251;t&#233;, &#224; tous, tant de peine. N&#8217;est-il pas vrai ?</p></blockquote><p class="alinea">Malgr&#233; le souhait d&#8217;&#201;corcheville, <em>La Revue </em><em><span class="petitecap">sim</span></em> dispara&#238;tra, mais pas pour longtemps puisqu&#8217;elle donnera naissance &#224; deux nouveaux organismes en 1917 et 1920. Pendant la guerre, les anciens de <em>La Revue </em><em><span class="petitecap">sim</span></em> dont Lionel de La Laurencie, vont cr&#233;er la Soci&#233;t&#233; fran&#231;aise de musicologie (<span class="petitecap">sfm</span>) sur les ruines de la Soci&#233;t&#233; internationale de musique et publieront un <em>Bulletin </em>qui deviendra la <em>Revue de musicologie. </em>Loin de l&#8217;actualit&#233;, s&#8217;&#233;cartant d&#233;lib&#233;r&#233;ment du contexte sociopolitique et culturel, la <span class="petitecap">sfm</span> et son <em>Bulletin </em>favoriseront une approche tr&#232;s &#171;&#160;scientifique&#160;&#187; et relativement nouvelle en France, de la musicologie, bien qu&#8217;encore teint&#233;e par les tendances historicisantes &#224; la mani&#232;re de la Schola Cantorum et &#233;cartant pour un temps toute la musicologie germanique. En parall&#232;le, sous les auspices du musicologue Henry Pruni&#232;res qui s&#8217;&#233;carte r&#233;solument de la <span class="petitecap">sfm</span>, est cr&#233;&#233;e <em>La Revue musicale</em>. C&#8217;est &#224; partir d&#8217;un r&#233;seau international qui place la musicologie fran&#231;aise au coeur de l&#8217;action musicale contemporaine que Pruni&#232;res &#233;tablit de nouvelles alliances avec le milieu des arts et de la litt&#233;rature pour fonder l&#8217;une des plus c&#233;l&#232;bres revues musicales de la premi&#232;re moiti&#233; du <span class="petitecap">xx</span><sup>e</sup>&#160;si&#232;cle. &#192; partir de documents in&#233;dits, nous &#233;tudierons les circonstances qui m&#232;nent &#224; la refondation de <em>La Revue musicale</em> sur les cendres de la <em>Revue </em><em><span class="petitecap">sim</span></em> entre 1915 et 1919. Nous verrons ainsi comment les hasards de la guerre m&#232;nent Pruni&#232;res &#224; entreprendre la carri&#232;re d&#8217;&#233;diteur et comment le musicologue con&#231;oit le projet international de la revue dans un contexte de guerre qui contribue &#224; une red&#233;finition des cultures nationales.</p><p class="alinea">Il est difficile d&#8217;extrapoler sur ce qu&#8217;aurait pu &#234;tre l&#8217;avenir de <em>La Revue musicale </em><em><span class="petitecap">sim</span></em> si la guerre n&#8217;avait pas eu lieu. Il est par contre possible de documenter et de comprendre le r&#244;le que la Grande Guerre jouera dans l&#8217;essor d&#8217;une nouvelle dynamique pour la musicologie fran&#231;aise dont la division d&#8217;abord justifi&#233;e par le conflit aura des cons&#233;quences &#224; long terme sur l&#8217;&#233;chiquier international de la discipline.</p>""" # noqa

    @with_value('1056320ar.xml', 'get_abstracts', html=True)
    def test_can_convert_renvoi_to_footnote_links(self, value):
        assert value[0]['content'] == """<p class="alinea"><em>Vu son expertise en classe et dans l&#8217;&#233;cole, l&#8217;enseignant associ&#233; est consid&#233;r&#233; comme une personne essentielle &#224; la formation initiale en enseignement. Des attentes &#224; son &#233;gard sont formul&#233;es par les instances minist&#233;rielles (gouvernement du Qu&#233;bec, 2002, 2008), mais aussi par les stagiaires (Caron, Portelance &amp; Martineau, 2013). Pour r&#233;pondre, l&#8217;enseignant associ&#233; est fortement incit&#233; &#224; s&#8217;inscrire dans un processus de formation continue, ce qui lui permet d&#8217;enrichir ses pratiques de formateur du stagiaire. Dans le but de soutenir le d&#233;veloppement des comp&#233;tences attendues des enseignants associ&#233;s (Portelance, Gervais, Lessard, Beaulieu et al, 2008), une recherche subventionn&#233;e par le minist&#232;re de l&#8217;&#201;ducation du Qu&#233;bec</em>&#160;<a href="#no1" id="re1no1" class="norenvoi">[1]</a><em> utilise une approche collaborative avec une communaut&#233; de pratique compos&#233;e d&#8217;enseignants associ&#233;s. Les membres sont engag&#233;s dans une d&#233;marche de r&#233;flexion et de coconstruction de sens (Bourassa, Philion &amp; Chevalier, 2007). Les discussions portent sur les pratiques d&#8217;encadrement du stagiaire. L&#8217;analyse de leurs propos met en &#233;vidence les manifestations de la dynamique interactionnelle qui favorise leur cod&#233;veloppement professionnel.</em></p>"""  # noqa


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
        assert value['fr'] == ['formation &#224; l&#8217;enseignement',
                               '<span class=""><em>postures en formation</em></span>',
                               'rapport &#224; l&#8217;&#233;valuation', 'rapport au savoir']


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
            "scope": "numero",
            "content": ["Une version ant&#233;rieure de ce texte &#224; &#233;t&#233; publi&#233;e dans <em>Le Devoir </em>du 7 mars 2011."]  # noqa
        }]

    @with_value('1006460ar.xml', 'get_notegens')
    def test_can_return_its_notegen_with_links(self, value):
        assert value == [{
            "type": "edito",
            "scope": "numero",
            "content": ['Pour obtenir la liste des sigles utilis&#233;s dans cet article et les r&#233;f&#233;rences compl&#232;tes aux oeuvres de Marie-Claire Blais, <a href="http://www.erudit.org/revue/vi/2011/v37/n1/1006456ar.html">voir p.&#160;7</a>.']  # noqa
        }]

    @with_value('1007816ar.xml', 'get_notegens')
    def test_can_return_its_notegen_with_biography(self, value):
        assert value == [{
            "type": "edito",
            "scope": "numero",
            "content": ["Sophie Th&#233;riault est professeure &#224; la Facult&#233; de droit de l&#8217;Universit&#233; d&#8217;Ottawa, Section de droit civil. Elle est &#233;galement membre du Barreau du Qu&#233;bec, du Centre du droit de l&#8217;environnement et de la durabilit&#233; mondiale de l&#8217;Universit&#233; d&#8217;Ottawa et du Centre de recherche et d&#8217;enseignement sur les droits de la personne de l&#8217;Universit&#233; d&#8217;Ottawa. David Robitaille est professeur &#224; la Facult&#233; de droit de l&#8217;Universit&#233; d&#8217;Ottawa, Section de droit civil. Il est &#233;galement membre du Barreau du Qu&#233;bec et du Centre de recherche et d&#8217;enseignement sur les droits de la personne de l&#8217;Universit&#233; d&#8217;Ottawa. Cet article a &#233;t&#233; r&#233;alis&#233; gr&#226;ce &#224; l&#8217;appui financier de la Fondation du Barreau du Qu&#233;bec, que nous remercions vivement. Nos remerciements vont &#233;galement &#224; nos assistants de recherche Camille Provencher, Pierre-Alexandre Henri, Nora Szeles et Karine H&#233;bert, ainsi qu&#8217;&#224; notre coll&#232;gue S&#233;bastien Grammond, pour ses commentaires judicieux."]  # noqa
        }, {
            "type": "edito",
            "scope": "numero",
            "content": [
                "Citation: (2011) 57:2 McGill LJ 211",
                "R&#233;f&#233;rence&#160;: (2011) 57&#160;:&#160;2 RD McGill 211",
            ]
        }]

    @with_value('1038621ar.xml', 'get_notegens')
    def test_can_return_its_notegen_with_multiple_paragraphs(self, value):
        assert value == [{
            "type": "edito",
            "scope": "numero",
            "content": ["Le pr&#233;sent texte suscite un questionnement approfondi sur l&#8217;&#233;conomie du contrat. Le lecteur trouvera des &#233;l&#233;ments de r&#233;ponse dans le texte suivant&#160;: &#171;&#160;L&#8217;apport &#233;pist&#233;mologique de la notion d&#8217;&#233;conomie du contrat en mati&#232;re d&#8217;interpr&#233;tation&#160;&#187;, (2016) 57:4 C&#160;de&#160;D &#224; para&#238;tre en d&#233;cembre."]  # noqa
        }, {
            "type": "auteur",
            "scope": None,
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
        EXPECTED = "Esth&#233;tique et s&#233;miotique\xa0: Pr&#233;sentation / Aesthetics and Semiotics: Presentation"  # noqa
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
        references = self.test_objects['009255ar.xml'].get_references(html=False)
        assert references[0] == {'title': "Akenside, Mark. Poems. London: J. Dodsley, 1772.", 'doi': None}  # noqa
        assert len(references) == 53

        references = self.test_objects['1003507ar.xml'].get_references(html=False)
        assert references[3] == {'title': "Cheung, Martha P. Y. (2005): ‘To translate’ means ‘to exchange’? A new interpretation of the earliest Chinese attempts to define translation (‘fanyi’). Target. 17(1):27-48.", 'doi': '10.1075/target.17.1.03che'}  # noqa

    def test_can_return_references_with_markup(self):
        references = self.test_objects['009255ar.xml'].get_references()
        assert references[0] == {'title': "Akenside, Mark.  <em>Poems</em>.  London: J. Dodsley, 1772.", 'doi': None}  # noqa
        assert len(references) == 53

    def test_html_body(self):
        html = self.test_objects['1001948ar.xml'].get_html_body()
        assert 'Ferreira' in html


@with_fixtures('./eruditarticle/tests/fixtures/article/savant/minimal', EruditArticle)
class TestArticleSavantMinimal(object):

    def test_can_return_titles_and_subtitles(self):
        from eruditarticle.objects.base import Title
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
        assert self.test_objects['49222ac.xml'].get_reviewed_works(html=False) == ["Love and Death on Long Island (Rendez-vous à Long Island), Grande-Bretagne / Canada, 1997, 93 minutes"]  # noqa


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
