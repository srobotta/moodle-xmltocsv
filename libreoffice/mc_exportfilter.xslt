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

<xsl:template match="table:table">
  <!-- Process all table-rows after the column labels in table-row 1 -->
  <xsl:for-each select="table:table-row">
    <xsl:if test="position()>1">
      <xsl:if test="./table:table-cell[3]/*">
        <question type="multichoice">
          <name>
            <text><xsl:value-of select="./table:table-cell[3]"/></text>
          </name>
          <questiontext format="moodle_auto_format">
            <text><xsl:value-of select="./table:table-cell[4]"/></text>
          </questiontext>
          <generalfeedback format="html">
            <text></text>
          </generalfeedback>
          <defaultgrade>1.0000000</defaultgrade>
          <penalty>0.3333333</penalty>
          <hidden>0</hidden>
          <idnumber></idnumber>
          <single>true</single>
          <shuffleanswers>false</shuffleanswers>
          <answernumbering>none</answernumbering>
          <showstandardinstruction>0</showstandardinstruction>
          <correctfeedback format="html">
            <text></text>
          </correctfeedback>
          <partiallycorrectfeedback format="html">
            <text></text>
          </partiallycorrectfeedback>
          <incorrectfeedback format="html">
            <text></text>
          </incorrectfeedback>
          <shownumcorrect/>
          <answer format="html">
            <xsl:attribute name="fraction"><xsl:value-of select="./table:table-cell[6]"/></xsl:attribute>
            <text>
              <xsl:call-template name="text">
                <xsl:with-param name="content">
                  <xsl:value-of select="./table:table-cell[5]"/>
                </xsl:with-param>
              </xsl:call-template>
            </text>
            <feedback format="html">
              <text></text>
            </feedback>
          </answer>
          <answer format="html">
            <xsl:attribute name="fraction"><xsl:value-of select="./table:table-cell[8]"/></xsl:attribute>
            <text>
              <xsl:call-template name="text">
                <xsl:with-param name="content">
                  <xsl:value-of select="./table:table-cell[7]"/>
                </xsl:with-param>
              </xsl:call-template>
            </text>
            <feedback format="html">
              <text></text>
            </feedback>
          </answer>
          <answer format="html">
            <xsl:attribute name="fraction"><xsl:value-of select="./table:table-cell[10]"/></xsl:attribute>
            <text>
              <xsl:call-template name="text">
                <xsl:with-param name="content">
                  <xsl:value-of select="./table:table-cell[9]"/>
                </xsl:with-param>
              </xsl:call-template>
            </text>
            <feedback format="html">
              <text></text>
            </feedback>
          </answer>
          <answer format="html">
            <xsl:attribute name="fraction"><xsl:value-of select="./table:table-cell[12]"/></xsl:attribute>
            <text>
              <xsl:call-template name="text">
                <xsl:with-param name="content">
                  <xsl:value-of select="./table:table-cell[11]"/>
                </xsl:with-param>
              </xsl:call-template>
            </text>
            <feedback format="html">
              <text></text>
            </feedback>
          </answer>
        </question>
      </xsl:if>
    </xsl:if>
  </xsl:for-each>
</xsl:template>

</xsl:stylesheet>
