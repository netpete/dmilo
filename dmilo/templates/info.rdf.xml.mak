<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="http://127.0.0.1:9000/style/info.xsl"?>
<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
	xmlns:dc="http://purl.org/dc/elements/1.1/">
<rdf:Description rdf:about="file://${model.filename}">
   <dc:title>${model.name}</dc:title>
   <dc:creator>${model.creator}</dc:creator>
   <dc:type>${model.type}</dc:type>
% for tag in tags.split(','): 
   <dc:subject>${tag}</dc:subject>
% endfor
</rdf:Description>
</rdf:RDF>

