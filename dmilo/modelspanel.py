"""
	Module for the Model display panel.	

	@Author: Peter Tiegs
	Nascentia Corporation 2007 (Some Rights Reserved).
	"""
	
__author__="Peter Tiegs"
import wx
import os
import sys
import pkg_resources
from modelstore import Model
from twisted.internet import threads

class thumbList(wx.ListCtrl):
	"""The list control displaying the models in the database"""
	def __init__(self, **kwargs):
		p = wx.PreListCtrl()
		self.PostCreate(p)
		self.Bind(wx.EVT_WINDOW_CREATE, self.OnCreate)

	def OnCreate(self, evt):
		wx.LogDebug("thumbList.OnCreate")
		if self is evt.GetEventObject():
			self.Unbind(wx.EVT_WINDOW_CREATE)
			wx.LogDebug( "Creating %r from %r"%(self, evt))
			self.thumbs = wx.ImageList(91,91, True )
			self.AssignImageList(self.thumbs, wx.IMAGE_LIST_NORMAL)
			thumbfile = pkg_resources.resource_filename('dmilo', 'resource/nothumb.png')
			## Load the file
			modelimage = wx.Image(thumbfile, wx.BITMAP_TYPE_PNG)
			## Scale the image to 91 by 91
			height = (91 * modelimage.GetHeight())/modelimage.GetWidth()
			modelimage.Rescale(91,int(height))
			modelbmp = wx.BitmapFromImage(modelimage)
			modelbmp.SetSize((91,91))
			index = self.thumbs.Add(modelbmp)
			for model in Model.select():
				index = self.thumbs.Add(modelbmp)
			self.display(Model.select())
			self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected)
			#self.loadThumbnails()
			d = threads.deferToThread(self.loadThumbnails).addCallback(self.thumbsLoaded).addErrback(self.thumbLoadErr)
		else:
			evt.Skip()

	def thumbsLoaded(self, val):
		wx.LogMessage( "ThumbsLoaded")

	def thumbLoadErr(self, val):
		wx.LogError( "error Loading Thumbs %r"%(val))

	def loadThumbnails(self):
		wx.LogDebug('loadThumbnails')
		models = Model.select()
		for model in models:
			self.addThumbnail(model)
		wx.LogDebug('Done Loading Thumbnails')
		return models


	def addThumbnail(self, model):
		"""Add an individual model to the image the list.
			@model: a reference to a Model"""
		## check to see if the thumbnail file exists.
		#wx.LogDebug('addThumbnail %s'%(model.thumb))
		if not os.path.exists(model.thumb):
			rsr = os.path.splitext(model.thumb)[0]+".rsr"
			if not os.path.exists(rsr):
				thumbfile = pkg_resources.resource_filename('dmilo', 'resource/nothumb.png')
			else:
				thumbfile = pkg_resources.resource_filename('dmilo', 'resource/rsrthumb.png')
		else:
			thumbfile = model.thumb
		## Load the file
		try:
			#wx.LogMessage(thumbfile)
			modelimage = wx.Image(thumbfile, wx.BITMAP_TYPE_PNG)
		except:
			wx.LogError("unable to load image %s"%(modelimage))
			raise
		## Scale the image to 91 by 91
		if not modelimage.IsOk():
			thumbfile = pkg_resources.resource_filename('dmilo', 'resource/nothumb.png')
			try:
				modelimage = wx.Image(thumbfile, wx.BITMAP_TYPE_PNG)
			except:
				wx.LogError("unable to load image %s"%(modelimage))
				raise
			
		try:
			height = (91 * modelimage.GetHeight())/modelimage.GetWidth()
			modelimage.Rescale(91,int(height))
		except (wx.PyAssertionError):
			wx.LogError("Unable to get width or height from %r\nImage ok %r"%(modelimage,modelimage.IsOk()))
			raise
		wx.CallAfter(self.updateBitmap, modelimage, model)

	def updateBitmap(self, modelimage, model):
		modelbmp = wx.BitmapFromImage(modelimage)
		modelbmp.SetSize((91,91))
		try:
			## The file to the list
			index = self.thumbs.Replace(int(model.id)-1, modelbmp)
		except (wx.PyAssertionError), inst :
			wx.LogError("""
			Model.id: %s out of Range.  Length of thumbs is %s, %r
			"""%(model.id, self.thumbs.GetImageCount(), self.thumbs))
			raise	
			

		
	def display(self, models):
		""" Show all the models in the selection.
			@models: SQLObject iterator for the selection of models.
			"""
		self.ClearAll()	
		for model in models:
			lIndex = self.InsertImageStringItem(model.id ,model.name, model.id-1 )

	def idFromIndex(self, index):
		"""Get the DB id of a model based on its position in the list.
		This is needed because the Image list is does not have any
		members available for storing additional data.
			@index: index into the Imagelist.
		"""
		return self.GetItem(index).GetImage() +1

	def OnItemSelected(self, event):
		"""Item Selected event is passed up to the containing panel."""
		event.Skip()

	

