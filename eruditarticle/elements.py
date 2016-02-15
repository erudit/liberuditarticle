# -*- coding: utf-8 -*-

import sys

from lxml import etree


def _cleantag(tag):
    # * lxml shows tags concatenated with their namespaces in the
    # * form {http://namespace}tag so a split must be performed
    return tag.split('}')[1]


class Struct(dict):
    """dot.notation access to dictionary attributes"""
    def __getattr__(self, attr):
        return self.get(attr)
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


def _select_element(treeobj, tag):
    selected = None
    if treeobj.objtree() is not None:
        for item in treeobj.objtree().iter():
            if _cleantag(item.tag) == tag:
                selected = item
                break

    # if selected is None:
    #   print("Warning: element \"%s\" not found in the datastream. Creating a dummy node." % (tag))
    return selected


class Element():

    def __init__(self, treeobj):
        self._attributes = Struct()
        self._treeobj = treeobj
        self._children = Struct()
        self.ch = self.children

        # * import attributes
        if self._treeobj is not None:
            for attrib in self._treeobj.attrib:
                self.attr(attrib, self._treeobj.attrib[attrib])

    def objtree(self):
        return self._treeobj

    def children(self):
        return self._children

    def attr(self, *args):
        if self._treeobj is not None:
            if len(args) == 0:
                # return self._attributes
                return self._attributes
            if len(args) == 1:
                try:
                    return self._attributes[args[0]]
                except KeyError:
                    return None
            if len(args) == 2:
                # console.debug(self._attributes)
                self._attributes[args[0]] = args[1]
        else:
            return None

    def innerxml(self):
        if self._treeobj is not None:
            string = ""
            for s in etree.tostring(self._treeobj).decode("utf-8").split("\n")[1:-2]:
                string += s+"\n"
            return string
        else:
            return None

    def text(self):
        if self._treeobj is not None:
            return ''.join(self._treeobj.itertext())
        else:
            return None

    def addchild(self, tag):
        self.children()[tag] = Element(_select_element(self, tag))
        self.__dict__[tag] = self.children()[tag]

        # * this may fix the problem of many instances of an element
        # * requires that _select_element returns an iterable of selected instances.
        # if tag in self.children():
        #     self.children()[tag].append( Element( _select_element(self, tag)  ) )
        # else:
        #     self.children()[tag] = [Element( _select_element(self, tag)  )]
        #     self.__dict__[tag] = self.children()[tag][0]


class Article(Element):
    """
    An EruditArticle manager
    """

    def populatefrom(self, child, taglist):
        """Populate a child with subchilds"""
        if child is not None:
            for _m in taglist:
                # console.debug(parent.children(), _m)
                # child.children()[_m] = Element( _select_element(child, _m)  )
                child.addchild(_m)

    def __init__(self, xmlstring):
        super().__init__(etree.fromstring(xmlstring))
        self.datatree = self._treeobj

        xmlschemaattrib = '{http://www.w3.org/2001/XMLSchema-instance}schemaLocation'
        erudit3xsd = 'http://www.erudit.org/xsd/article http://www.erudit.org/' \
            'xsd/article/3.0.0/eruditarticle.xsd'

        if xmlschemaattrib in self.attr():
            if self.attr(xmlschemaattrib) == erudit3xsd:
                iserudit3 = True
            else:
                iserudit3 = False
        else:
            iserudit3 = False

        if not iserudit3:
            print("Not an EruditArticle datastream!")
            sys.exit()

        # * Extraction of ERUXDS300 sections
        # * /article
        self.populatefrom(self, ['admin', 'liminaire', 'corps', 'partiesann'])

        # * ********** ADMIN *************************************************
        # * /article/admin
        self.populatefrom(
            self.admin,
            ['diffnum', 'droitsauteur', 'editeur', 'histpapier', 'infoarticle',
             'numero', 'prod', 'prodnum', 'revue', 'schema'])

        # * /article/admin/infoarticle
        self.populatefrom(
            self.admin.infoarticle,
            ['grdescripteur', 'idpublic', 'manifestation', 'nbaudio', 'nbeq',
             'nbfig', 'nbimage', 'nbmot', 'nbnote', 'nbom', 'nbpage', 'nbpara',
             'nbrefbiblio', 'nbtabl', 'nbvideo', 'pagination', ])

        # * /article/admin/revue
        self.populatefrom(
            self.admin.revue,
            ['directeur', 'grdescripteur', 'idissn', 'idissnnum',
             'redacteurchef', 'sstitrerev', 'sstitrerevparal', 'titrerev',
             'titrerevabr', 'titrerevabrparal', 'titrerevparal', ])

        # * /article/admin/numero
        self.populatefrom(
            self.admin.numero,
            ['anonumero', 'grtheme', 'idisbn', 'idisbn13', 'idisbnnum',
             'idisbnnum13', 'nonumero', 'notegen', 'pub', 'pubnum', 'volume', ])

        # * ********** LIMINAIRE ***********************************************
        # * /article/liminaire
        self.populatefrom(
            self.liminaire,
            ['erratum', 'grauteur', 'grmotcle', 'grtitre', 'notegen', 'resume'])

        # * /article/liminaire/grtitre
        self.populatefrom(
            self.liminaire.grtitre,
            ['sstitre', 'sstitreparal', 'surtitre', 'surtitre2', 'surtitre3',
             'surtitreparal', 'surtitreparal2', 'surtitreparal3', 'titre',
             'titreparal', 'trefbiblio', ])

        # * /article/liminaire/grauteur
        # ! CHECK HERE BECAUSE IT COULD APPEAR MANY auteur's
        self.populatefrom(self.liminaire.grauteur, ['auteur'])

        # ! ALSO MANY grmotcle coud appear

        # * ********** CORPS     ***********************************************
        # * /article/corps <-- left as it *is*

        # * ********** PARTIESANN **********************************************
        # * /article/partiesann
        self.populatefrom(
            self.partiesann,
            ['grannexe', 'grbiblio', 'grnote', 'grnotebio', 'merci'])

        # console.log("children", self.children())
        # console.log( self.children().corps.attr())
