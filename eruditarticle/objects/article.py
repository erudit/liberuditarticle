import logging
from collections import OrderedDict
from xml.etree import ElementTree

from .base import EruditBaseObject
from .mixins import CopyrightMixin
from .mixins import ISBNMixin
from .mixins import ISSNMixin
from .mixins import PublicationPeriodMixin
from .person import (
    Person, format_authors, format_authors_mla, format_authors_apa, format_authors_chicago
)

from .exceptions import InvalidOrdseqError, InvalidTitleLevelError

logger = logging.getLogger(__name__)


class EruditArticle(PublicationPeriodMixin, ISBNMixin, ISSNMixin, CopyrightMixin, EruditBaseObject):

    def get_abstracts(self, formatted=False, html=False, strip_footnotes=True):
        """ Returns the abstracts of the article object
        :param formatted: (bool, optional): Defaults to False.
            Not applicable
        :param html: (bool, optional): Defaults to False.
        :param strip_footnotes: (bool, optional): Defaults to True.
            If the abstracts are to be displayed outside the context of the article (i.e. in the
            issue summary) where the footnotes are not accessible, we may want to strip footnotes
            links from the abstracts. If `html` is False, footnotes will always be stripped.

        :returns: a list of dictionaries of the form::

            abstracts = [
                {
                    'content': '...',
                    'lang': 'fr',
                    'typeresume': ''
                    'type': 'main'
                },
            ]

        """
        abstracts = []
        languages = self.get_languages()

        # If html is False, footnotes should always be stripped.
        if not html:
            strip_footnotes = True
        # If strip_footnotes is True, strip `renvoi` elements from abstracts.
        strip_footnotes = ['renvoi'] if strip_footnotes else []

        if html:
            parser_method = self.convert_marquage_content_to_html
        else:
            parser_method = self.stringify_children
        for abstract_dom in self.findall('resume'):

            abstract = {
                'lang': abstract_dom.get('lang'),
                'typeresume': abstract_dom.get('typeresume'),
                'title': parser_method(
                    abstract_dom.find('titre'),
                    strip_elements=[] + strip_footnotes,
                ),
                'content': parser_method(
                    abstract_dom,
                    strip_elements=['titre'] + strip_footnotes,
                ),
            }

            try:
                if languages.index(abstract["lang"]) == 0:
                    abstract["type"] = "main"
                else:
                    abstract["type"] = "paral"
            except ValueError:
                abstract["type"] = "equivalent"

            abstracts.append(abstract)

        return sorted(
            abstracts,
            key=lambda x: languages.index(x['lang']) if x['lang'] in languages else 10
        )

    def get_article_type(self):
        """ :returns: the type of the article. """
        return self._dom.getroot().get('typeart')

    def get_authors(self, formatted=False, html=False, style=None, suffixes=True):
        """ :returns: the authors of the article object.

            :param formatted: Whether we return a formatted string or a Person list
            :param html: if formatted, whether we include HTML markup
            :param style: alternative formatting style. choices: 'mla', 'apa', 'chicago'
        """

        authors = [
            Person(author) for author in
            self._root.xpath('//liminaire//auteur[not(contribution[@typecontrib!="aut"])]')
        ]

        if formatted and len(authors) == 0:
            return ""
        elif formatted:
            if style == 'mla':
                authors = format_authors_mla(authors)
            elif style == 'apa':
                authors = format_authors_apa(authors)
            elif style == 'chicago':
                authors = format_authors_chicago(authors)
            else:
                authors = format_authors(authors, html=html, suffixes=suffixes)

        return authors

    def get_formatted_authors(self):
        """
        .. warning::
           Will be removed or modified 0.3.0
           For more information please refer to :py:mod:`eruditarticle.objects`

        :returns: the formatted author names of the article object.
        """
        return self.get_authors(formatted=True)

    def get_notegens(self, html=True):
        """

        :returns: the notes of the article object. """
        notegen_nodes = self.findall('notegen')
        notegens = []
        if html:
            parser_method = self.convert_marquage_content_to_html
        else:
            parser_method = self.stringify_children
        for notegen_node in notegen_nodes:
            notegen = {}
            alinea_nodes = self.findall("alinea", dom=notegen_node)
            notegen['type'] = notegen_node.get('typenoteg')
            notegen['scope'] = notegen_node.get('porteenoteg')
            notegen["content"] = [parser_method(n) for n in alinea_nodes]
            notegens.append(notegen)
        return notegens

    def get_doi(self):
        """ :returns: the DOI of the article object. """
        doi = self.get_text('infoarticle/idpublic[@scheme="doi"]')
        return doi.strip() if doi is not None else None

    def get_uri(self):
        """ :returns: the URI of the article object. """
        return self.get_text('idpublic[@scheme="uri"]')

    def get_first_page(self):
        """ :returns: the first page of the article object. """
        return self.get_text('infoarticle//pagination//ppage')

    def get_html_body(self):
        """
        .. warning::
           Will be removed or modified 0.3.0
           For more information please refer to :py:mod:`eruditarticle.objects`

        :returns: the full body of the article object as HTML text. """
        alinea_nodes = self.findall('para/alinea')
        if alinea_nodes:
            nodes = [
                self.convert_marquage_content_to_html(n) for n in alinea_nodes if n.text is not None
            ]
            html_body = ' '.join(n for n in nodes if n is not None)
        else:
            texte_node = self.find('corps/texte')
            html_body = self.convert_marquage_content_to_html(texte_node)
        return html_body if html_body else ''

    def get_html_title(self):
        """
        .. warning::
           Will be removed or modified in 0.3.0
           For more information please refer to :py:mod:`eruditarticle.objects`

        :returns: the title of the article object with HTML tags. """
        return self.convert_marquage_content_to_html(self.find('titre'))

    def get_keywords(self, formatted=False, html=False):
        """ :returns: the keywords of the article object.

        The keywords are returned as an ``OrderedDict`` index by language code.
        """
        keywords = OrderedDict()
        for tree_keywords in self.findall('grmotcle'):
            lang_keywords = keywords[tree_keywords.get('lang')] = []
            for n in tree_keywords.findall('motcle'):
                if html:
                    s = self.convert_marquage_content_to_html(n)
                else:
                    s = ElementTree.tostring(n, encoding='utf8', method='text')
                    s = s.decode('utf-8').strip()
                lang_keywords.append(s)
        return keywords

    def get_languages(self):
        """ :returns: a list of  languages of the article object. """
        return self._root.get('lang').split()

    def get_language(self):
        """ :returns: the main language of the article. """
        languages = self.get_languages()
        if languages:
            return languages[0]

    def get_last_page(self):
        """ :returns: the last page of the article object. """
        return self.get_text('infoarticle//pagination//dpage')

    def get_ordseq(self):
        """ :returns: the ordering number of the article object. """
        ordseq = self._root.get('ordseq')
        try:
            return int(ordseq) if ordseq is not None else 0
        except ValueError:
            raise InvalidOrdseqError("ordseq needs to be a positive integer")

    def get_processing(self):
        """ :returns: the processing type of the article object. """
        return self._root.get('qualtraitement')

    def get_publication_year(self):
        """ :returns: the year of publication of the article object. """
        return self.get_text('numero//pub//annee')

    def get_publishers(self):
        """ :returns: the publisher of the article object. """
        return [
            publisher.text
            for publisher in self.findall('editeur//nomorg')
        ]

    def get_section_titles(self, level=1, html=True):
        """ :returns: the section titles of the article object

            :param title_type: type of the title (main or paral)
            :param level: level of the section title (1, 2 or 3)
            :param html: True if special characters should be converted to html entities
        """
        if level not in (1, 2, 3):
            raise InvalidTitleLevelError("Level should be 1, 2 or 3")

        section_title = self._get_section_title(level=level, html=html)

        surtitre_elem = 'surtitreparal{}'.format(
            "" if level == 1 else level
        )

        if html:
            parser_method = self.convert_marquage_content_to_html
        else:
            parser_method = self.stringify_children

        paral_titles = self.find_paral(
            self.find('liminaire//grtitre'),
            surtitre_elem,
        )
        for lang, title in paral_titles.items():
            paral_titles[lang] = parser_method(title)

        return {
            'main': section_title,
            'paral': paral_titles,
        } if section_title else None

    def _get_section_title(self, level=1, html=True):
        """ :returns: the section title of the article object. """
        element = 'liminaire//grtitre//surtitre{}'.format(
            "" if level == 1 else level
        )
        if html:
            return self.convert_marquage_content_to_html(self.find(element))
        else:
            return self.stringify_children(self.find(element))

    def get_subtitle(self):
        """ :returns: the subtitle of the article object. """
        return self.stringify_children(self.find('sstitre'))

    def get_reviewed_works(self, html=True):
        """ :returns: the works reviewed by this article """
        return self._get_reviewed_or_referenced_works(
            root_elem=self._dom, ref_elem_name='trefbiblio', html=html
        )

    def get_references(self, html=True):
        """
        .. warning::
           Will be removed or modified 0.3.0
           For more information please refer to :py:mod:`eruditarticle.objects`

         :returns: the works referenced by this article. returns a dictionary
             that contains possibly two keys: doi and title
        """
        references = []
        xml_references = self.findall('refbiblio')
        for reference in xml_references:
            doi = reference.find('idpublic[@scheme="doi"]')
            if doi is not None:
                doi = doi.text.strip()
            if html:
                title = self.convert_marquage_content_to_html(
                    reference, strip_elements=('idpublic',)
                )
            else:
                title = self.stringify_children(reference, strip_elements=('idpublic',))
            references.append({'doi': doi, 'title': title})
        return references

    def get_title(self, formatted=False, html=False):
        """ Returns the title of the article object.
        :param formatted: (bool, optional): Defaults to False.
            Not applicable
        :param html: (bool, optional): Defaults to False.
        """
        if formatted:
            return self._get_formatted_title(html=html)
        else:
            return self.stringify_children(
                self.find('titre', dom=self.find('grtitre')),
                strip_elements=['liensimple', 'renvoi']
            )

    def get_journal_titles(self):
        """ :returns: the titles of the journal

        This method has the same behaviour as :meth:`~.get_titles`.
        """
        languages = self.find('revue').get('lang').split()

        return self._get_titles(
            root_elem=self.find('revue'),
            title_elem_name='titrerev',
            subtitle_elem_name='sstitrerev',
            paral_title_elem_name='titrerevparal',
            paral_subtitle_elem_name='sstitrerevparal',
            languages=languages,
        )

    def get_titles(self, html=True):
        """ Retrieve the titles of an article

        .. warning::
           The interface of this method will be modified in 0.3.0
           For more information please refer to :py:mod:`eruditarticle.objects`

        :returns: a dict containing all the titles and subtitles of the object.

        Titles are grouped in four categories: ``main``, ``paral``, ``equivalent`` and
        ``reviewed_works``, where  ``main`` is the title proper, ``paral`` the
        parallel titles proper, and ``equivalent`` the original titles in a language
        different from that of the title proper. Parallel titles accompanies an article
        body in the specified language, while equivalent titles do not have an
        accompanying article body.

        The value for ``main`` is an Title namedtuple. The value for ``paral`` and
        ``equivalent`` is a list of Title namedtuples. The value for
        ``reviewed_works`` is a list of strings. Items in ``paral`` are ordered
        by the position of their ``lang`` attribute in the main ``<article>``. Items in
        ``equivalent`` are ordered by their position in the XML document.

        Here is an example of a return value::

            titles = {
                'main': Title(
                    title='Serge Emmanuel Jongué',
                    subtitle='Capter et narrer l'indicible',
                    lang='fr',
                },
                'paral': [
                    Title(
                        title='Serge Emmanuel Jongué',
                        subtitle='Capturing and Narrating the Unspeakable',
                        lang='en'
                    )
                ],
                'equivalent': [
                    Title(
                    title='la lorem ipsum dolor sit amet',
                    subtitle='la sub lorem ipsum',
                    lang='es',
                ],
                reviewed_works=[],
            }

        While the ``lang`` attribute of each ``<titreparal>`` tag is specified explicitely,
        the ``lang`` of the main title is not specified in the XML document. It is assumed
        to be the first value of ``lang`` in the ``<article>`` tag.

        If the article is ill-defined and specifies a subtitle for a given language without
        specifying a corresponding title, this subtitle will be ignored.

        Ref: http://www.erudit.org/xsd/article/3.0.0/doc/eruditarticle_xsd.html#article

        """

        titles = self._get_titles(
            root_elem=self.find('grtitre'),
            title_elem_name='titre',
            subtitle_elem_name='sstitre',
            paral_title_elem_name='titreparal',
            paral_subtitle_elem_name='sstitreparal',
            languages=self.get_languages(),
            html=html,
        )

        titles['reviewed_works'] = self.get_reviewed_works(html=html)
        return titles

    def get_formatted_journal_title(self):
        """
        .. warning::
           Will be removed or modified 0.3.0
           For more information please refer to :py:mod:`eruditarticle.objects`

        Format the journal title

        :returns: the formatted journal title

        Calls :meth:~.get_journal_titles` and format its results.
        """
        titles = self.get_journal_titles()
        return self._get_formatted_single_title(titles, use_equivalent=True)

    def _get_formatted_title(self, html=True):
        """ Format the article titles

        .. warning::
           Will be removed or modified 0.3.0
           For more information please refer to :py:mod:`eruditarticle.objects`

        :returns: the formatted article title

        This method calls :meth:`~.get_titles` and format its results.

        The result is formatted in the following way::

            "{main_title} : {main_subtitle} / .. /  {paral_title_n} : {paral_subtitle_n} / {reviewed_works}"  # noqa

        If an article title is in French, a non-breaking space is inserted after the colon
        separating it from its subtitle.
        """
        titles = self.get_titles(html=html)
        formatted_title = self._get_formatted_single_title(titles)

        if titles['reviewed_works']:
            reviewed_works = " / ".join(
                reference for reference in titles['reviewed_works']
            )

            if formatted_title:
                formatted_title = "{title} / {reviewed_works}".format(
                    title=formatted_title,
                    reviewed_works=reviewed_works
                )
            else:
                formatted_title = reviewed_works
        return formatted_title

    def get_formatted_title(self):
        """
        .. warning::
           Will be removed or modified 0.3.0
           For more information please refer to :py:mod:`eruditarticle.objects`
        """
        return self._get_formatted_title(html=False)

    def get_formatted_html_title(self):
        """
        .. warning::
           Will be removed or modified 0.3.0
           For more information please refer to :py:mod:`eruditarticle.objects`
        """
        return self._get_formatted_title(html=True)

    @property
    def is_of_type_roc(self):
        # If the first "corps/texte" element of the article is of type "roc" that means that
        # its content is minimally processed. What that's the case, this property is True.
        # Created for the purpose of fixing support#198
        texte_node = self.find('corps/texte')
        return texte_node is not None and texte_node.get('typetexte') == 'roc'

    abstracts = property(get_abstracts)
    article_type = property(get_article_type)
    authors = property(get_authors)
    reviewed_works = property(get_reviewed_works)
    doi = property(get_doi)
    uri = property(get_uri)
    first_page = property(get_first_page)
    html_body = property(get_html_body)
    html_title = property(get_html_title)
    keywords = property(get_keywords)
    languages = property(get_languages)
    language = property(get_language)
    last_page = property(get_last_page)
    ordseq = property(get_ordseq)
    processing = property(get_processing)
    publication_year = property(get_publication_year)
    publishers = property(get_publishers)
    subtitle = property(get_subtitle)
    title = property(get_title)
    titles = property(get_titles)
