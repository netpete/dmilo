<html>
	<head>
		<title>dMilo Websharing</title>
	</head>
	<body>
		<table>
		<%
			rows = modelsPerPage/modelsPerRow
			rem = modelsPerPage%modelsPerRow
			if rem:
				rows = rows +1
		%>
		% for row in range(rows):
			<tr>
				  % for model in list(models)[(row*modelsPerRow):(row*modelsPerRow)+modelsPerRow]:

					  <td>
						  <ul>
							  <li><a href="info/${model.id}"><img src="thumbnail/${model.id}.png" alt="${model.id}"/></a></li>
							  <li>${model.name}</li>
						  </ul>
					  </td>
				  % endfor
			</tr>
		% endfor
		</table>
<div>

% if prev >= 0:

<a href="?next=${prev}">&lt;&lt;Prev</a>

% endif
<a href="?next=${next}">Next&gt;&gt;</a></div>
	</body>
</html>
