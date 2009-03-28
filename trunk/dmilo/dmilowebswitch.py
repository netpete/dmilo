import wx
from wx import xrc
from twisted.internet import reactor
from webview import webShare
class WebSwitch( object ):
	webShare= webShare(reactor)

	def init_frame( self, frame ):
		self.frame = frame
		self.radioSwitch = xrc.XRCCTRL( self.frame, 'ID_WEBSWITCH' )
		self.frame.Bind( wx.EVT_RADIOBOX, self.OnEvent, self.radioSwitch) 

	def OnEvent( self, evt ):
		actions = [self.webShare.startShare, self.webShare.stopShare]
		actions[evt.GetInt()]()

		evt.Skip()
		
