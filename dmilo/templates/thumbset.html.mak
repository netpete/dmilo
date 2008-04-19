<html>
	<head>
		<title>dMilo Websharing</title>
	</head>
	<body>
		<ul>
		% for model in models:

			<li><a href="info/${model.id}"><img src="thumbnail/${model.id}.png" alt=${model.id}/></a>
			
			${model.filename}</li>
		% endfor
		</ul>
<div>

% if prev >= 0:

<a href="?next=${prev}">&lt;&lt;Prev</a>

% endif
<a href="?next=${next}">Next&gt;&gt;</a></div>
	</body>
</html>
