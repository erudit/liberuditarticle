<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="html" indent="yes" encoding="UTF-8"/>

<xsl:template match="resume/titre"></xsl:template>

<xsl:template match="alinea | refbiblio">
    <p class="{name()}">
        <xsl:apply-templates/>
    </p>
</xsl:template>

<xsl:template match="bloccitation | verbatim">
    <blockquote class="{name()}">
        <xsl:apply-templates/>
    </blockquote>
</xsl:template>

<xsl:template match="listenonord">
    <xsl:variable name="signe" select="@signe"/>
    <xsl:choose>
        <xsl:when test="@nbcol">
            <!-- listenonord multi-colonnes -->
            <xsl:variable name="elemlistes" select="elemliste"/>
            <xsl:variable name="nbElems" select="count($elemlistes)"/>
            <xsl:variable name="nbCols" select="@nbcol"/>
            <xsl:variable name="divClass" select="concat('nbcol', $nbCols)"/>
            <xsl:variable name="quotient" select="floor($nbElems div $nbCols)"/>
            <xsl:variable name="reste" select="$nbElems mod $nbCols"/>
            <!-- maximum 5 colonnes -->
            <div class="multicolonne">
                <xsl:variable name="arret1" select="$quotient + number($reste &gt; 0)"/>
                <div class="{$divClass}">
                    <ul class="{$signe}">
                        <xsl:for-each select="elemliste[position() &gt; 0 and position() &lt;= $arret1]">
                            <xsl:apply-templates select="."/>
                        </xsl:for-each>
                    </ul>
                </div>
                <xsl:if test="$nbCols &gt;= 2">
                    <xsl:variable name="arret2" select="$arret1 + $quotient + number($reste &gt; 1)"/>
                    <div class="{$divClass}">
                        <ul class="{$signe}">
                            <xsl:for-each select="elemliste[position() &gt; $arret1 and position() &lt;= $arret2]">
                                <xsl:apply-templates select="."/>
                            </xsl:for-each>
                        </ul>
                    </div>
                    <xsl:if test="$nbCols &gt;= 3">
                        <xsl:variable name="arret3" select="$arret2 + $quotient + number($reste &gt; 2)"/>
                        <div class="{$divClass}">
                            <ul class="{$signe}">
                                <xsl:for-each select="elemliste[position() &gt; $arret2 and position() &lt;= $arret3]">
                                    <xsl:apply-templates select="."/>
                                </xsl:for-each>
                            </ul>
                        </div>
                        <xsl:if test="$nbCols &gt;= 4">
                            <xsl:variable name="arret4" select="$arret3 + $quotient + number($reste &gt; 3)"/>
                            <div class="{$divClass}">
                                <ul class="{$signe}">
                                    <xsl:for-each select="elemliste[position() &gt; $arret3 and position() &lt;= $arret4]">
                                        <xsl:apply-templates select="."/>
                                    </xsl:for-each>
                                </ul>
                            </div>
                            <xsl:if test="$nbCols &gt;= 5">
                                <xsl:variable name="arret5" select="$arret4 + $quotient + number($reste &gt; 4)"/>
                                <div class="{$divClass}">
                                    <ul class="{$signe}">
                                        <xsl:for-each select="elemliste[position() &gt; $arret4 and position() &lt;= $arret5]">
                                            <xsl:apply-templates select="."/>
                                        </xsl:for-each>
                                    </ul>
                                </div>
                            </xsl:if>
                        </xsl:if>
                    </xsl:if>
                </xsl:if>
            </div>
        </xsl:when>
        <xsl:otherwise>
            <!-- listenonord 1 colonne -->
            <ul class="{@signe}">
                <xsl:apply-templates/>
            </ul>
        </xsl:otherwise>
    </xsl:choose>
</xsl:template>

<xsl:template match="listeord">
    <xsl:variable name="numeration" select="@numeration"/>
    <xsl:variable name="start">
        <xsl:choose>
            <xsl:when test="@compteur">
                <xsl:value-of select="@compteur"/>
            </xsl:when>
            <xsl:otherwise>1</xsl:otherwise>
        </xsl:choose>
    </xsl:variable>
    <xsl:choose>
        <xsl:when test="@nbcol">
            <!-- listeord multi-colonnes -->
            <xsl:variable name="elemlistes" select="elemliste"/>
            <xsl:variable name="nbElems" select="count($elemlistes)"/>
            <xsl:variable name="nbCols" select="@nbcol"/>
            <xsl:variable name="divClass" select="concat('nbcol', $nbCols)"/>
            <xsl:variable name="quotient" select="floor($nbElems div $nbCols)"/>
            <xsl:variable name="reste" select="$nbElems mod $nbCols"/>
            <!-- maximum 5 colonnes -->
            <div class="multicolonne">
                <xsl:variable name="arret1" select="$quotient + number($reste &gt; 0)"/>
                <div class="{$divClass}">
                    <ol class="{$numeration}" start="{$start}">
                        <xsl:for-each select="elemliste[position() &gt; 0 and position() &lt;= $arret1]">
                            <xsl:apply-templates select="."/>
                        </xsl:for-each>
                    </ol>
                </div>
                <xsl:if test="$nbCols &gt;= 2">
                    <xsl:variable name="arret2" select="$arret1 + $quotient + number($reste &gt; 1)"/>
                    <div class="{$divClass}">
                        <ol class="{$numeration}" start="{$start + $arret1}">
                            <xsl:for-each select="elemliste[position() &gt; $arret1 and position() &lt;= $arret2]">
                                <xsl:apply-templates select="."/>
                            </xsl:for-each>
                        </ol>
                    </div>
                    <xsl:if test="$nbCols &gt;= 3">
                        <xsl:variable name="arret3" select="$arret2 + $quotient + number($reste &gt; 2)"/>
                        <div class="{$divClass}">
                            <ol class="$numeration" start="{$start + $arret2}">
                                <xsl:for-each select="elemliste[position() &gt; $arret2 and position() &lt;= $arret3]">
                                    <xsl:apply-templates select="."/>
                                </xsl:for-each>
                            </ol>
                        </div>
                        <xsl:if test="$nbCols &gt;= 4">
                            <xsl:variable name="arret4" select="$arret3 + $quotient + number($reste &gt; 3)"/>
                            <div class="{$divClass}">
                                <ol class="$numeration" start="{$start + $arret3}">
                                    <xsl:for-each select="elemliste[position() &gt; $arret3 and position() &lt;= $arret4]">
                                        <xsl:apply-templates select="."/>
                                    </xsl:for-each>
                                </ol>
                            </div>
                            <xsl:if test="$nbCols &gt;= 5">
                                <xsl:variable name="arret5" select="$arret4 + $quotient + number($reste &gt; 4)"/>
                                <div class="{$divClass}">
                                    <ol class="$numeration" start="{$start + $arret4}">
                                        <xsl:for-each select="elemliste[position() &gt; $arret4 and position() &lt;= $arret5]">
                                            <xsl:apply-templates select="."/>
                                        </xsl:for-each>
                                    </ol>
                                </div>
                            </xsl:if>
                        </xsl:if>
                    </xsl:if>
                </xsl:if>
            </div>
        </xsl:when>
        <xsl:otherwise>
            <!-- listeord 1 colonne -->
            <xsl:element name="ol">
                <xsl:attribute name="class">
                    <xsl:value-of select="@numeration"/>
                </xsl:attribute>
                <xsl:if test="@compteur">
                    <xsl:attribute name="start">
                        <xsl:value-of select="$start"/>
                    </xsl:attribute>
                </xsl:if>
                <xsl:apply-templates/>
            </xsl:element>
        </xsl:otherwise>
    </xsl:choose>
</xsl:template>

<xsl:template match="elemliste">
    <li>
        <xsl:apply-templates/>
    </li>
</xsl:template>

<xsl:template match="liensimple">
    <xsl:choose>
        <!-- Only convert <liensimple> to <a> if parent node is not <titre>. -->
        <xsl:when test="name(parent::node()) != 'titre'">
            <a href="{@href}"><xsl:apply-templates/></a>
        </xsl:when>
        <!-- Otherwise, only display <liensimple> text. -->
        <xsl:otherwise>
            <xsl:apply-templates/>
        </xsl:otherwise>
    </xsl:choose>
</xsl:template>

<xsl:template match="a|A">
    <!-- Add 'href' to '<a>' tags. Convert '<A>' to '<a>' -->
    <a href="{@href}"><xsl:apply-templates/></a>
</xsl:template>

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
    <xsl:element name="a">
        <xsl:attribute name="href">
            <xsl:text>#</xsl:text><xsl:value-of select="@idref"/>
        </xsl:attribute>
        <xsl:attribute name="id">
            <xsl:value-of select="@id"/>
        </xsl:attribute>
        <xsl:attribute name="class">
            <xsl:text>norenvoi</xsl:text>
        </xsl:attribute>
        <xsl:text>[</xsl:text>
        <xsl:value-of select="normalize-space()"/>
        <xsl:text>]</xsl:text>
    </xsl:element>
</xsl:template>

<xsl:template match="exposant">
    <sup>
        <xsl:apply-templates/>
    </sup>
</xsl:template>

<xsl:template match="indice">
    <sub>
        <xsl:apply-templates/>
    </sub>
</xsl:template>

<xsl:template match="*">
    <xsl:copy>
        <xsl:apply-templates/>
    </xsl:copy>
</xsl:template>

</xsl:stylesheet>
