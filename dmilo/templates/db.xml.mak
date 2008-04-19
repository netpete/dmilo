<?xml version ="1.0"?>
<dmilo src="${db.file}">

<rdf:RDF
	xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax=ns#"
	xmlns:dc="http://purl.org/dc/element/1.1/">

% for model in models:
	<rdf:Description>
		<dc:title><![CDATA[${model.name}]]></dc:title>
		<dc:identifier><![CDATA[${model.filename}]]></dc:identifier>
		<dc:type>${model.type}</dc:type>
		<dc:creator>${model.creator}</dc:creator>
		<dc:subject>
%for tag in model.tags:
	${tag.tagname} 
%endfor
		</dc:subject>
		<dc:license>
			<readme>${model.readme}</readme>
			${model.license}
		</dc:license>
		<thumbnail><![CDATA[${model.thumb}]]></thumbnail>
	</rdf:Description>
% endfor
</rdf:RDF>

</dmilo>
