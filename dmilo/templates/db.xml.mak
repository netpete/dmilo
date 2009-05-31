<?xml version ="1.0"?>
<dmilo src="${dbfile}">

<rdf:RDF
	xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax=ns#"
	xmlns:dc="http://purl.org/dc/element/1.1/">
	
	<rdf:Description about="file://${model.filename}">
		<dc:title>${model.name}</dc:title>
		<dc:identifier>${model.filename}</dc:identifier>
		<dc:type>${model.type}</dc:type>
		<dc:creator>${model.creator}</dc:creator>
		<dc:license>
			<readme>${model.readme}</readme>
			${model.license}
		</dc:license>
% for tag in model.tags:
		<dc:subject>${tag.tagname}</dc:subject>
% endfor
		<thumbnail><dc:description>file://${model.thumb.filename}</dc:description></thumbnail>
	</rdf:Description>

</rdf:RDF>
</dmilo>
