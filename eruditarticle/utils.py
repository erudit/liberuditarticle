# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import io
import re

import lxml.etree as et


drop_namespace_xslt = '''<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
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
    """ Given an lxml tree object, remove all XML namespaces. """
    xslt_doc = et.parse(io.StringIO(drop_namespace_xslt))
    transform = et.XSLT(xslt_doc)
    return transform(treedom)


def normalize_whitespace(s):
    """ Returns `s` with all whitespaces deduplicated and normalized

    That is, newlines and tabs converted to space.
    """
    if not s:
        return s
    return re.sub(r'[ \n\t]+', ' ', s.strip())
