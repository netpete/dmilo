<?xml version="1.0" encoding="UTF-8"?>
<xsl:transform version="1.0" 
	xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
	xmlns:dc="http://purl.org/dc/elements/1.1/"
	xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
<xsl:template match="/">
<html xmlns:dc="http://purl.org/dc/elements/1.1/">
	<head>
		<title>:<xsl:apply-templates select="//dc:title"/></title>
	</head>
	<body>
		<div>
			<div>
				Name:<xsl:apply-templates select="//dc:title"/> 
			</div>
			<div>Creator: <xsl:apply-templates select="//dc:creator"/> </div>
			<div>Type: <xsl:apply-templates select="//dc:type"/> </div>
			<div>
			Filename: <xsl:apply-templates select="//Description/@about"/>
			</div>
			<div>Tags: <xsl:apply-templates select="//dc:subject"/></div>
		</div>
	</body>
</html>
</xsl:template>
<xsl:template match="//dc:title">
	<span property="dc:title"><xsl:value-of select="."/></span>
</xsl:template>
<xsl:template match="//dc:creator">
	<span property="dc:creator"><xsl:value-of select="."/></span>
</xsl:template>
<xsl:template match="//dc:type">
	<span property="dc:type"><xsl:value-of select="."/></span>
</xsl:template>
<xsl:template match="//rdf:Description/@about">
	<xsl:value-of select="." />
</xsl:template>
<xsl:template match="//dc:subject">
	<xsl:for-each select=".">
		<span property="dc:subject"><xsl:value-of select="." /></span>,
	</xsl:for-each>
</xsl:template>

</xsl:transform>
