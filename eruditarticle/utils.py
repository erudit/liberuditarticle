# -*- coding: utf-8 -*-

from __future__ import unicode_literals
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


def remove_xml_namespaces(treedom):
    """
    Given an lxml tree object, remove all XML namespaces.
    """
    xslt_doc = et.parse(io.StringIO(xslt))
    transform = et.XSLT(xslt_doc)
    return transform(treedom)
