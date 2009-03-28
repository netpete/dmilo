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

VIEWABLE_THUMB_COUNT = 1000

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
			self.thumbs = wx.ImageList(91,91, True, VIEWABLE_THUMB_COUNT+1 )
			self.AssignImageList(self.thumbs, wx.IMAGE_LIST_NORMAL)
			
			thumbfile = pkg_resources.resource_filename('dmilo', 'resource/nothumb.png')
			## Load the file
			modelimage = wx.Image(thumbfile, wx.BITMAP_TYPE_PNG)
			## Scale the image to 91 by 91
			height = (91 * modelimage.GetHeight())/modelimage.GetWidth()
			modelimage.Rescale(91,int(height))
			modelbmp = wx.BitmapFromImage(modelimage)
			modelbmp.SetSize((91,91))
			for i in  range(VIEWABLE_THUMB_COUNT):
				index = self.thumbs.Add(modelbmp)
			self.modelmap = []
			self.display(Model.select()[:VIEWABLE_THUMB_COUNT])
			self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected)
			
		else:
			evt.Skip()

	def thumbsLoaded(self, val):
		wx.LogMessage( "ThumbsLoaded")

	def thumbLoadErr(self, val):
		wx.LogError( "error Loading Thumbs %r"%(val))
		
	def loadThumbnails(self):
		wx.LogDebug('loadThumbnails')
		models = Model.select()
		#for id in range(1, VIEWABLE_THUMB_COUNT):
		#	self.addThumbnailFromDB( Model.selectBy(id=id).getOne())
		wx.LogDebug('Done Loading Thumbnails')
		return models

	def addThumbnailFromDB(self, model, position=0):
		buffer = model.thumb.bitmap
		modelimage = wx.ImageFromData(model.thumb.width,model.thumb.height, model.thumb.bitmap)

		if not modelimage.IsOk():
			print "ERROR"
			
		modelbmp = wx.BitmapFromImage(modelimage)
		modelbmp.SetSize((91,91))
		wx.CallAfter(self.thumbs.Replace, position, modelbmp)

		
	def addThumbnail(self, model):
		"""Add an individual model to the image the list.
			@model: a reference to a Model"""
		## check to see if the thumbnail file exists.
		#wx.LogDebug('addThumbnail %s'%(model.thumb))
		if not os.path.exists(model.thumb.filename):
			rsr = os.path.splitext(model.thumb.filename)[0]+".rsr"
			if not os.path.exists(rsr):
				thumbfile = pkg_resources.resource_filename('dmilo', 'resource/nothumb.png')
			else:
				thumbfile = pkg_resources.resource_filename('dmilo', 'resource/rsrthumb.png')
		else:
			thumbfile = model.thumb.filename
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
			#index = self.thumbs.Replace(int(model.id)-1, modelbmp)
			index = self.thumbs.Replace(1, modelbmp)
		except (wx.PyAssertionError), inst :
			wx.LogError("""
			Model.id: %s out of Range.  Length of thumbs is %s, %r
			"""%(model.id, self.thumbs.GetImageCount(), self.thumbs))
			raise	

	def GetViewableItems(self):
		wx.LogDebug("Enter")
		retVal = []
		for item in range(100):
			if self.isViewable(item):
				retVal.append(item)
		wx.LogDebug("Exit")
		return retVal

	def isViewable(self, item):
		pos = self.GetItemPosition(item)
		return pos[0] <= 1000
		
	def display(self, models):
		""" Show all the models in the selection.
			@models: SQLObject iterator for the selection of models.
			"""
		wx.LogDebug("Enter display")
		self.ClearAll()
		self.modelmap = []
		count = 0
		for model in models[:VIEWABLE_THUMB_COUNT]:
	 		self.addThumbnailFromDB(model, position = count)
	 		self.InsertImageStringItem(model.id ,model.name, count)
	 		#self.InsertImageStringItem(model.id ,str(model.id), count)
	 		count = count +1
			self.modelmap.append((model.id, count))
				
		self.SetItemState(0, wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED)
		wx.LogDebug("Exit display")

	def idFromIndex(self, index):
		"""Get the DB id of a model based on its position in the list.
		This is needed because the Image list is does not have any
		members available for storing additional data.
			@index: index into the Imagelist.
		"""
		return self.modelmap[index][0]

	def OnItemSelected(self, event):
		"""Item Selected event is passed up to the containing panel."""
		event.Skip()
	def GetItemAtUpperLeft(self, increment=0):
		colWidth = 105
		itemShift = (increment/colWidth)*self.GetCountPerPage()
		return (((self.GetItemPosition(0)[0]/colWidth)*self.GetCountPerPage()) - itemShift) * -1
		
	def OnScrollChange(self, evt):
		inc = self.sw.CalcScrollInc(evt)
		lc =self.GetItemAtUpperLeft(inc*self.sw.GetScrollPixelsPerUnit()[0])

		print "lc = ",lc
		if self.modelmap[lc][1] == VIEWABLE_THUMB_COUNT:
			count = 1
			offset = 0
			for offset in range(VIEWABLE_THUMB_COUNT-1):
				model = Model.selectBy(id=self.idFromIndex(lc+offset))[0]
				print offset, self.idFromIndex(lc+offset), model.name
				self.addThumbnailFromDB(model, position = offset+1)
				self.SetItemImage(lc+offset, offset+1, offset+1)
				self.RefreshItem(lc+offset)
	
		evt.Skip()
