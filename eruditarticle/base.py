# -*- coding: utf-8 -*-

import io

import lxml.etree as et


xslt = '''<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="xml" indent="no"/>

<xsl:template match="/|comment()|processing-instruction()">
    <xsl:copy>
      <xsl:apply-templates/>
    </xsl:copy>
</xsl:template>

<xsl:template match="*">
    <xsl:element name="{local-name()}">
      <xsl:apply-templates select="@*|node()"/>
    </xsl:element>
</xsl:template>

<xsl:template match="@*">
    <xsl:attribute name="{local-name()}">
      <xsl:value-of select="."/>
    </xsl:attribute>
</xsl:template>
</xsl:stylesheet>
'''


class EruditBaseObject(object):
    def __init__(self, xmlstring):
        self._dom = self._remove_namespaces(et.fromstring(xmlstring))

    def __getattr__(self, name):
        try:
            val = super(EruditBaseObject, self).__getattr__(name)
        except AttributeError:
            pass
        else:
            return val

        # Tries to fetch the value of the tag whose name
        # matches the considered attribute
        result = self.find(name)
        if result is None:
            raise AttributeError

        return result

    def find(self, tag_name):
        """Find an element in the tree."""
        return self._dom.find('.//{}'.format(tag_name))

    def findall(self, tag_name):
        """Find elements in the tree."""
        return self._dom.findall('.//{}'.format(tag_name))

    def get_text(self, tag_name):
        """Returns the text associated with the considered tag."""
        result = self.find(tag_name)
        return result.text if result is not None else None

    def get_text_from_tags(self, tag_names):
        """Returns the first text value associated with a list of potential tags."""
        text = None
        for tname in tag_names:
            text = self.get_text(tname)
            if text:
                break
        return text

    def _remove_namespaces(self, dom):
        xslt_doc = et.parse(io.StringIO(xslt))
        transform = et.XSLT(xslt_doc)
        return transform(dom)
