__author__='Peter Tiegs'
import wx
from modelstore import VirtualDir, Catalog
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

	def addSubdirs(self, parent, vdir):
		cat = Catalog.selectBy(id=vdir.catalog)
		subs = []
		if cat.count() >0: 
			subs = cat[0].subdirs
		for sub in subs:
			child = self.AppendItem(parent, sub.dirname.capitalize())
			self.SetItemPyData(child, sub.id)
			self.addSubdirs(child, sub)

	def addDirs(self, rootdir):
		retval = self.AddRoot(rootdir)
		for vroot in VirtualDir.selectBy(root=True):
			treeChild = self.AppendItem(retval, vroot.dirname.capitalize())
			self.SetItemPyData(treeChild, vroot.id)
			self.addSubdirs(treeChild, vroot)

		return retval
		
