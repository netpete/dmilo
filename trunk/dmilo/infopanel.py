"""
	Module for the Asset information display Panel.	

	@Author: Peter Tiegs
	Nascentia Corporation 2007 (Some Rights Reserved).
	"""
	
__author__="Peter Tiegs"

import wx.html
from webview import infoTemplate

class infoPanel(wx.Panel):
	"""The Panel containing the info block HTML window."""
	def __init__(self):
		"""Panel Constructor.
			@size: the size of the panel
		"""
		p = wx.PrePanel()
		
		self.PostCreate(p)
		self.Bind(wx.EVT_WINDOW_CREATE, self.OnCreate)
		self.Bind(wx.EVT_SIZE, self.OnSize)
	def OnCreate(self, evt):
		if self is evt.GetEventObject():
			self.infoText=wx.html.HtmlWindow(self, -1, size=self.GetSize())
			self.sizer = wx.BoxSizer(wx.VERTICAL)
			self.SetSizer(self.sizer)
			self.sizer.Add(self.infoText, 1)
		evt.Skip()

	def OnSize(self, evt):
		if hasattr(self, 't'):
			sz= self.GetSize()
			w, h = self.t.GetTextExtent(self.t.GetLabel())
			self.t.SetPosition(((sz.width-w)/2, (sz.height-h)/2))

	def displayInfo(self,  model):
		"""Display the information about the model.
			@model: The model to display.
		"""
		taglist = []
		for tag in model.tags:
			taglist.append(tag.tagname)
		self.infoText.SetPage(infoTemplate.render(model=model,  tags= ','.join(taglist)))

class InfoFrame(wx.MiniFrame):
	"""A mini frame to display the info panel in a seperate window."""
	def __init__(self, parent):
		"""Frame Constructor."""
		wx.MiniFrame.__init__(self, parent, -1,"Info", pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE)
		self.info =infoPanel(self, -1, self.GetSize())
		self.Bind(wx.EVT_CLOSE, self.OnClose)
	def OnClose(self, event):
		"""Capture wx.EVT_CLOSE event to preserve the handle to the frame.
		"""
		self.Show(False)
