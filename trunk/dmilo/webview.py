"""Web view provides access to html templates used by the webview mode of dMilo.  It also provides
the twisted web configuration for the webview.
	@Author: Peter Tiegs
	Nascentia Corporation 2007 (Some Rights Reserved.)"""
import os
import pkg_resources
from twisted.web import resource
from mako.template import Template
from modelstore import Model, Tag
## Template for list of thumnails.
setTemplate = Template(pkg_resources.resource_string('dmilo','templates/thumbset.html.mak')) 
## Template for item metadata.
infoTemplate = Template(pkg_resources.resource_string('dmilo','templates/info.html.mak')) 
## Template for Tagcloud.
tagcloudTemplate = Template(pkg_resources.resource_string('dmilo','templates/tagcloud.html.mak')) 
modelsPerPage = 5 #10
class SetView(resource.Resource):
	"""Provides a view of a set of thumnails."""
	isLeaf = True
	def render_GET(self, req):
		list = ''
		models = Model.select()
		start = 0
		print req.args
		if req.args.has_key('next'):
			start = int(req.args['next'][0])
		elif req.args.has_key('tag'):
			models = Tag.selectBy(tagname=req.args['tag'][0]).getOne().models
		end = start + modelsPerPage
		prev = start - modelsPerPage
		outtext = setTemplate.render_unicode(models=models[start:end], next=end, prev=prev).encode('UTF-8')
		return outtext

class thumbnail(resource.Resource):
	""" Displays the Thumbnail image."""
	isLeaf = True
	def render(self, req):
		imagefile = req.postpath[0]
		index = imagefile.split('.')[0]
		models = Model.selectBy(id=int(index))
		thumb = ''
		for each in models:
			thumb= each.thumb
		req.setHeader('content-type', 'image/png')
		imagedata = open(str(thumb), 'rb')
		return imagedata.read()

class infoView(resource.Resource):
	""" Provides the basic view of an inidividual items metadata."""
	isLeaf = True
	def render_GET(self, req):
		model = Model.selectBy(id = int(req.postpath[0])).getOne()
		temp = model.filename.split('/')
		temp.reverse()
		name = temp[0]
		taglist= []
		for tag in model.tags:
			taglist.append(tag.tagname)
		tags = ','.join(taglist)
		outstring = infoTemplate.render_unicode(name=name, model=model, tags =tags).encode('utf-8')
		return outstring
class tagView(resource.Resource):
	""" Provides the tag cloud view. """
	isLeaf=True
	def render_GET(self, req):
		tags = Tag.select()
		outstring = tagcloudTemplate.render_unicode(tags=tags).encode('utf-8')
		return outstring

class webShare(object):
	""" The web service for dMilo web Sharing.""" 
	port = 9000
	def __init__(self, reactor):
		self.reactor = reactor
	def startShare(self):
		from twisted.web import server
		root = resource.Resource()
		root.putChild('', SetView())
		root.putChild('thumbnail', thumbnail())
		root.putChild('info', infoView())
		root.putChild('tags', tagView())
		site = server.Site(root)
		self.reactor.listenTCP(self.port, site)

	def stopStare(self):
		pass


	
