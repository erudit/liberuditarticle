# -*- coding: utf-8 -*-

import io

import lxml.etree as et


marquage_to_html = et.XSLT(et.parse(io.StringIO(
    '''<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="html" indent="yes" encoding="UTF-8"/>
<xsl:strip-space elements="*"/>

<xsl:template match="marquage">
    <xsl:choose>
        <xsl:when test="@typemarq='gras'">
            <strong>
                <xsl:apply-templates/>
            </strong>
        </xsl:when>
        <xsl:when test="@typemarq='italique'">
            <em>
                <xsl:apply-templates/>
            </em>
        </xsl:when>
        <xsl:when test="@typemarq='taillep'">
            <small>
                <xsl:apply-templates/>
            </small>
        </xsl:when>
        <xsl:otherwise>
            <span class="{@typemarq}">
                <xsl:apply-templates/>
            </span>
        </xsl:otherwise>
    </xsl:choose>
</xsl:template>

<xsl:template match="renvoi">
</xsl:template>

<xsl:template match="*">
    <xsl:copy>
        <xsl:apply-templates/>
    </xsl:copy>
</xsl:template>

</xsl:stylesheet>
''')))
