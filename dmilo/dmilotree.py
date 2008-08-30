__author__='Peter Tiegs'
import wx
class RuntimeTree(wx.TreeCtrl):
	def __init__(self, *args, **kwargs):
		p = wx.PreTreeCtrl()
		self.PostCreate(p)
		self.Bind(wx.EVT_WINDOW_CREATE, self.OnCreate)

	def OnCreate(self, evt):
		if self is evt.GetEventObject():
			self.Unbind(wx.EVT_WINDOW_CREATE)
		else:
			evt.Skip()
		
