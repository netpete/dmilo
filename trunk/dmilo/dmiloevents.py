import wx

class NewTagEvent(wx.PyCommandEvent):
	def __init__(self, evtType, id):
		wx.PyCommandEvent.__init__(self, evtType, id)
		self.tagName =''

	def GetTagName(self):
		return self.tagName

	def SetTagName(self, tagName):
		self.tagName = tagName

dmEVT_NEW_TAG = wx.NewEventType()
EVT_NEW_TAG = wx.PyEventBinder(dmEVT_NEW_TAG, 1)

class AddThumbnailEvent(wx.PyCommandEvent):
	def __init__(self, evtType, id):
		wx.PyCommandEvent.__init__(self, evtType, id)
		self.modelID = -1

	def GetModelID(self):
		return self.modelID

	def SetModelID(self, modelID):
		self.modelID = modelID

dmEVT_ADD_THUMBNAIL = wx.NewEventType()
EVT_ADD_THUMBNAIL = wx.PyEventBinder(dmEVT_ADD_THUMBNAIL)

class ReadDBEvent(wx.PyCommandEvent):
	def __init__(self, evtType, id):
		wx.PyCommandEvent.__init__(self, evtType, id)
dmEVT_READ_DB = wx.NewEventType()
EVT_READ_DB = wx.PyEventBinder(dmEVT_READ_DB)
