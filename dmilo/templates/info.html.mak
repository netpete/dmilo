<html xmlns:dc="http://purl.org/dc/elements/1.1/">
<head><title>${model.lib}:${model.name}</title></head>
<body>
<div about="${model.filename}">
	 <div>
	 Name:<span property="dc:title">${model.name}</span>
	 </div>
	 <div>Creator:<span property="dc:creator">${model.creator}</span></div>
	 <div>Type: <span property="dc:type">${model.type}</span></div>
	 <div>Filename: <span property="dc:identifier">${model.filename}</span></div>
	 <div>Tags:
% for tag in tags.split(','):
		<span property="dc:subject">${tag}</span>
% endfor
	</div>
</div>
</body>
</html>
