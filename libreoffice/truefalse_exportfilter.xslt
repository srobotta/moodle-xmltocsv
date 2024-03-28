<?xml version="1.0" encoding="UTF-8"?>
<!-- We must define several namespaces, because we need them to access -->
<!-- the document model of the in-memory OpenOffice.org document.      -->
<!-- If we want to access more parts of the document model, we must    -->
<!-- add there namesspaces here, too.                                  -->
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
	xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
	xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0"
	xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"
	exclude-result-prefixes="office table text">

<xsl:output method="xml" indent="yes" encoding="UTF-8" omit-xml-declaration="no"/>

<!-- Process the document model -->
<xsl:template match="/">
  <quiz>
    <!-- Process all tables -->
    <xsl:apply-templates select="//table:table"/>
  </quiz>
</xsl:template>

<!-- Template for CDATA sections in text nodes -->
<xsl:template name="text">
  <xsl:param name="content"/>
    <xsl:text disable-output-escaping="yes">
      &lt;![CDATA[
    </xsl:text>
    <xsl:value-of select="$content" disable-output-escaping="yes"/>
    <xsl:text disable-output-escaping="yes">
      ]]&gt;
    </xsl:text>
</xsl:template>

<!-- Template for the fraction value, checks for true and false or 0 and 1 -->
<xsl:template name="fraction">
  <xsl:param name="content"/>
  <xsl:param name="col"/>
  <xsl:choose>
    <xsl:when test="contains($content, 'True') or
                    contains($content, 'true') or
                    $content='1'">
      <xsl:choose>
        <xsl:when test="$col='true'">100</xsl:when>
        <xsl:otherwise>0</xsl:otherwise>
      </xsl:choose>
    </xsl:when>
    <xsl:otherwise>
      <xsl:choose>
        <xsl:when test="$col='true'">0</xsl:when>
        <xsl:otherwise>100</xsl:otherwise>
      </xsl:choose>
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>

<xsl:template match="table:table">
  <!-- Process all table-rows after the column labels in table-row 1 -->
  <xsl:for-each select="table:table-row">
    <xsl:if test="position()>1">
      <xsl:if test="./table:table-cell[3]/*">
        <question type="truefalse">
          <name>
            <text><xsl:value-of select="./table:table-cell[3]"/></text>
          </name>
          <questiontext format="html">
            <text>
              <xsl:call-template name="text">
                <xsl:with-param name="content">
                  <xsl:value-of select="./table:table-cell[4]"/>
                </xsl:with-param>
              </xsl:call-template>
            </text>
          </questiontext>
          <generalfeedback format="html">
            <text>
              <xsl:call-template name="text">
                <xsl:with-param name="content">
                  <xsl:value-of select="./table:table-cell[8]"/>
                </xsl:with-param>
              </xsl:call-template>
            </text>
          </generalfeedback>
          <defaultgrade>1.0000000</defaultgrade>
          <penalty>1</penalty>
          <hidden>0</hidden>
          <idnumber></idnumber>
          <answer format="html">
            <xsl:attribute name="fraction">
              <xsl:call-template name="fraction">
                <xsl:with-param name="content">
                  <xsl:value-of select="./table:table-cell[5]"/>
                </xsl:with-param>
                <xsl:with-param name="col">true</xsl:with-param>
              </xsl:call-template>
            </xsl:attribute>
            <text>true</text>
            <feedback format="html">
              <text>
                <xsl:call-template name="text">
                  <xsl:with-param name="content">
                    <xsl:value-of select="./table:table-cell[6]"/>
                  </xsl:with-param>
                </xsl:call-template>
              </text>
            </feedback>
          </answer>
          <answer format="html">
            <xsl:attribute name="fraction">
              <xsl:call-template name="fraction">
                <xsl:with-param name="content">
                  <xsl:value-of select="./table:table-cell[5]"/>
                </xsl:with-param>
                <xsl:with-param name="col">false</xsl:with-param>
              </xsl:call-template>
            </xsl:attribute>
            <text>false</text>
            <feedback format="html">
              <text>
                <xsl:call-template name="text">
                  <xsl:with-param name="content">
                    <xsl:value-of select="./table:table-cell[7]"/>
                  </xsl:with-param>
                </xsl:call-template>
              </text>
            </feedback>
          </answer>
        </question>
      </xsl:if>
    </xsl:if>
  </xsl:for-each>
</xsl:template>

</xsl:stylesheet>
