# -*- coding: utf-8 -*-

from eulfedora import models
from eulxml.xmlmap import XmlObject


class JournalDigitalObject(models.DigitalObject):
    CONTENT_MODELS = ['info:fedora/erudit-model:seriesCModel', ]
    publications = models.XmlDatastream('PUBLICATIONS', 'Publications', XmlObject)


class PublicationDigitalObject(models.DigitalObject):
    CONTENT_MODELS = ['info:fedora/erudit-model:publicationCModel', ]
    publication = models.XmlDatastream('PUBLICATION', 'Publication', XmlObject)
    summary = models.XmlDatastream('SUMMARY', 'Summary', XmlObject)
    coverpage = models.FileDatastream(
        'COVERPAGE', 'Coverpage', defaults={'mimetype': 'image/jpeg', })
    pages = models.XmlDatastream('PAGES', 'Pages', XmlObject)


class ArticleDigitalObject(models.DigitalObject):
    CONTENT_MODELS = ['info:fedora/erudit-model:unitCModel', ]
    erudit_xsd300 = models.XmlDatastream('ERUDITXSD300', 'Erudit XSD300', XmlObject)
    unit = models.XmlDatastream('UNIT', 'Unit', XmlObject)
    pdf = models.FileDatastream('PDF', 'PDF', defaults={'mimetype': 'application/pdf', })
