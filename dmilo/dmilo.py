#!/Library/Frameworks/Python.framework/Versions/Current/bin/python

"""
	The dMilo Application.  dMilo is used to manage a collection of 3D model assets in a variety of Formats.  It is based on Opensource technology.   	

	Usage: dmilo (-n)
	-n: Create a new Database.

	@Author: Peter Tiegs
	Nascentia Corporation 2007 (Some Rights Reserved).
	"""
	
__author__="Peter Tiegs"

import wx
from  wx import xrc
from twisted.internet import wxreactor
## Start using twisted as the WX event handler.
wxreactor.install()
from twisted.internet import reactor, threads
import pkg_resources
import sys
import os
import optparse 
from webview import webShare
from dmiloimport import scandir
from modelstore import Model, ModelStore, Tag, Collection, VirtualDir, Catalog
from tagcloudpanel import EVT_TAG_SELECT

from posertypes.posertypes import POSERTYPES

class xrcApp(wx.App):
	def OnInit(self):
		self.res = xrc.XmlResource(pkg_resources.resource_filename('dmilo', 'resource/dmilo.xrc'))
		self.init_frame()
		self.init_menu()
		logfile = open('dmilo.log', 'w')
		self.logger = wx.LogStderr()
		wx.Log.SetActiveTarget(self.logger)
		wx.LogMessage("Starting Log.")
		#wx.Log.GetActiveTarget().SetLogLevel(40)
		
		self.webShare= webShare(reactor)
		return True

	def init_frame(self):
		self.frame = self.res.LoadFrame(None, 'MainFrame')
		self.topPanel = xrc.XRCCTRL(self.frame, 'topPanel')
		self.cmdLine = xrc.XRCCTRL(self.frame, 'ID_CMDLINE')
		self.tagCloud = xrc.XRCCTRL(self.frame, 'ID_TAGCLOUD')
		self.infoPanel = xrc.XRCCTRL(self.frame, 'ID_INFO')
		self.thumbList = xrc.XRCCTRL(self.frame, 'ID_THUMBLIST')
		self.dirView = xrc.XRCCTRL(self.frame, 'ID_RUNTIMETREE')
		self.root = self.dirView.addDirs(u'RuntimeCollections')
		self.topPanel.Bind(wx.EVT_KEY_DOWN, self.OnKeyPress)
		self.frame.Bind(EVT_TAG_SELECT, self.OnTagClick)
		self.frame.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected)
		self.frame.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnDirSelectChange, self.dirView)
		self.frame.Show()

	def init_menu(self):
		self.frame.Bind(wx.EVT_MENU, self.OnMenuQuit, id=xrc.XRCID('ID_QUIT'))
		self.frame.Bind(wx.EVT_MENU, self.OnImport, id=xrc.XRCID('ID_IMPORT'))
		self.frame.Bind(wx.EVT_MENU, self.OnWebShare, id=xrc.XRCID('ID_WEB_SHARE'))
			
		self.SetMacExitMenuItemId(xrc.XRCID('ID_QUIT'))

	def OnDirSelectChange(self, evt):
		id=self.dirView.GetItemPyData( evt.GetItem())
		vdir =  VirtualDir.selectBy(id=id)[0]
		models = vdir.models
		for vID in vdir.getAllSubdirs():
			models.extend(VirtualDir.selectBy(id=vID)[0].models)	

		
		self.thumbList.display(models)

		
	def OnTagClick(self, evt):
		tagset = Tag.selectBy(tagname=evt.GetTagName())
		if 0 != tagset.count():
			tag = tagset.getOne()
			models = tag.models
		else:
			wx.LogMessage("No Tag by that name")
			models = Model.select()
		self.thumbList.display(models)
		
	def OnKeyPress(self, event):
		"""Key Press Event Handler."""
		if wx.WXK_ESCAPE == event.GetKeyCode():
			self.command.Show(True)
		event.Skip()

	def OnItemSelected(self, event):
		"""Selected Item Event Handler."""
		id = self.thumbList.idFromIndex(event.m_itemIndex)
		self.cmdLine.selected =[]
		if 1 <= self.thumbList.GetSelectedItemCount():
			listid = self.thumbList.GetFirstSelected()
			self.cmdLine.selected.append(self.thumbList.idFromIndex(listid))
			while listid != -1:
				listid = self.thumbList.GetNextSelected(listid)
				if listid != -1:
					self.selected.append(self.thumbList.idFromIndex(listid))
		self.infoPanel.displayInfo(Model.selectBy(id=id).getOne())
		event.Skip()

	def OnMenuQuit(self, evt):
		#: :TODO: stop reactor instead
		sys.exit()	

	def OnWebShare(self, evt):
		#: :TODO: Check if webshare is running and reverse
		if not self.webShare.started:
			self.webShare.startShare()
		else:
			self.webShare.stopShare()
		

	def OnImport(self, evt):
		imp_dlg = wx.DirDialog(self.frame, "Import Directory", style = wx.DD_DEFAULT_STYLE)
		imp_dlg.CenterOnScreen()
		models = Model.select()
		before = models.count()
		if imp_dlg.ShowModal() ==wx.ID_OK:
			wx.LogDebug( "Scanning %s"%imp_dlg.GetPath())
			d = threads.deferToThread(scandir, imp_dlg.GetPath()).addCallback(self.done, before)
			#ret = scandir(imp_dlg.GetPath())
			#self.done(ret, before)

		imp_dlg.Destroy()
	
	def done(self,ret, before):
		models = Model.select()
		after =models.count()
		thumbfile = pkg_resources.resource_filename('dmilo', 'resource/nothumb.png')
	
		modelimage = wx.Image(thumbfile, wx.BITMAP_TYPE_PNG)
		## Scale the image to 91 by 91
		height = (91 * modelimage.GetHeight())/modelimage.GetWidth()
		modelimage.Rescale(91,int(height))
		modelbmp = wx.BitmapFromImage(modelimage)
		modelbmp.SetSize((91,91))
		for model in models[ before : after]:
			index = self.thumbList.thumbs.Add(modelbmp)
			self.thumbList.addThumbnail(model)
		self.thumbList.display(models)
		self.tagCloud.displayTags(Tag.select(orderBy="tagname"))
		
		wx.LogDebug("Scan Done.")


def main():

	parser =optparse.OptionParser()
	parser.add_option('-n','--new', action='store_true', dest='newdb', default=False, help='Initialize a new Database')
	parser.add_option('-x', '--xrc', action='store_true', dest='useXRC', default=True, help='Read the XRC file for the layout')

	(options, args) = parser.parse_args()
	#: Set the Preferences.
	dotDmiloPath =  os.path.join(os.path.expanduser('~'), '.dmilo')
	dmPref = wx.Config('dmilo')
	if not os.path.exists(dotDmiloPath):
		os.makedirs(dotDmiloPath)
	if not dmPref.Exists('dbPath'):
		dmPref.Write('dbPath', os.path.join(dotDmiloPath, 'dmilo.db'))
	if options.newdb or not os.path.exists(dmPref.Read('dbPath')):
		ModelStore(dmPref.Read('dbPath')).newStore()
	ModelStore(dmPref.Read('dbPath'))
	dmPref.Set(dmPref)
	#: Start the Application
	if options.useXRC:
		app = xrcApp(False)
	
	#: Add the Application to the Event Loop.
	reactor.registerWxApp(app)

	#: Start the Event Loop.
	reactor.run()

if __name__== '__main__':
	main()
