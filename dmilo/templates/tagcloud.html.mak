<style type="text/css">
	.smallTag {font-size:small;}
</style>
<div>
% for tag in tags :
	<span class="smalltag"><a href="/?tag=${tag.tagname}"> ${tag.tagname}</a> </span> 
% endfor
</div>
