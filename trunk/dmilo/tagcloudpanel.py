"""A Tag Cloud Widget for wx.python.  <Currently targeted only at dMilo 3D Asset Manager.
	@Author: Peter Tiegs
	Nascentia Corporation 2007 (Some Rights Reserved.)"""
import wx.html
from urlparse import urlparse
from modelstore import Tag

class TagSelectEvent(wx.PyCommandEvent):
	def __init__(self, evtType, id):
		wx.PyCommandEvent.__init__(self, evtType, id)
		self.tagName = ''
	def GetTagName(self):
		return self.tagName

	def SetTagName(self, tagName):
		self.tagName = tagName
		
dmEVT_TAG_SELECT = wx.NewEventType()
EVT_TAG_SELECT = wx.PyEventBinder(dmEVT_TAG_SELECT, 1)

class tagCloudWindow(wx.html.HtmlWindow):
	"""Display the Tags as a set of links"""
	def __init__(self, parent, id, size):
		"""Initialize a tagCloud
		@size: wx.size object or an integer tuple.
		"""
		wx.html.HtmlWindow.__init__(self, parent, id, size = size)
	def OnLinkClicked(self, linkinfo):
		"""Queries the Tag table for the taglink and selects all them models with that tag."""
		## Get the tagname from the link.
		tagname =  urlparse(linkinfo.GetHref())[4].split('=')[1]
		
		evt = TagSelectEvent(dmEVT_TAG_SELECT, self.GetId())
		evt.SetTagName(tagname)
		self.GetEventHandler().ProcessEvent(evt)

class xtagCloudPanel(wx.Panel):
	def __init__(self):
		p = wx.PrePanel()

		self.PostCreate(p)
		self.Bind(wx.EVT_WINDOW_CREATE, self.OnCreate)
		self.Bind(wx.EVT_SIZE, self.OnSize)
	def OnCreate(self, evt):
		if self is evt.GetEventObject():
			self.tagLinks = tagCloudWindow(self,-1, (300,150))
			self.sizer = wx.BoxSizer(orient=wx.VERTICAL)
			self.SetSizer(self.sizer)
			self.sizer.Add(self.tagLinks, 1)
			self.displayTags(Tag.select(orderBy="tagname"))
		evt.Skip()

	def OnSize(self, evt):
		if hasattr(self, 't'):
			sz= self.GetSize()
			w, h = self.t.GetTextExtent(self.t.GetLabel())
			self.t.SetPosition(((sz.width-w)/2, (sz.height-h)/2))

	
	def displayTags(self, tags):
		"""Displays all the tags in the Tags in the tags parameter.
		@tags: a SQLObject iterator for the Tags table."""
		import webview 
		self.tagLinks.SetPage(webview.tagcloudTemplate.render(tags =tags))
		
class tagCloudPanel(wx.Panel):
	def __init__(self, parent, id, size):
		"""Initializes the tagCloudPanel and adds all widgets to it.
		@size: wx.size object or an integer tuple."""

		wx.Panel.__init__(self, parent, id, size=size)
		self.sizer = wx.StaticBoxSizer(wx.StaticBox(self, -1, "Tag Cloud"), wx.VERTICAL)
		self.SetSizer(self.sizer)
		self.tagLinks=tagCloudWindow(self, -1, size=size)
		self.sizer.Add(self.tagLinks, 1)
		self.sizer.Fit(self)
		self.displayTags(Tag.select(orderBy="tagname"))

	def displayTags(self, tags):
		"""Displays all the tags in the Tags in the tags parameter.
		@tags: a SQLObject iterator for the Tags table."""
		self.tagLinks.SetPage(tagcloudTemplate.render(tags =tags))
