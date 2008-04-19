
"""
	The Command line control and parser.	

	@Author: Peter Tiegs
	Nascentia Corporation 2007 (Some Rights Reserved).
	"""
	
__author__="Peter Tiegs"
import wx
from modelstore import Model, Tag
from tagcloudpanel import tagCloudPanel,  dmEVT_TAG_SELECT, TagSelectEvent
from ZestyParser import RE, Skip, Inf, ZestyParser 
from ZestyParser.Helpers import QuoteHelper
## Commandline tokens
action = RE(r'tag|find', group=0)
sp = RE(r'\s+')
quoted = QuoteHelper(quotes=''''"''')
inline = RE(r'\w+',group=0 )
words = Inf*((quoted | inline ) + Skip(sp))
command = action +Skip(sp) + words

def eval(expression):
	"""Return a list of parsed out tokens"""
	parser = ZestyParser(expression)
	return parser.scan(command)

class commandPanel(wx.Panel):
	def __init__(self):
		p = wx.PrePanel()

		self.PostCreate(p)
		self.Bind(wx.EVT_WINDOW_CREATE, self.OnCreate)
	
	def OnCreate(self, evt):
		if self is evt.GetEventObject():
			self.selected = []
			self.sizer = wx.BoxSizer(wx.HORIZONTAL)
			self.SetSizer(self.sizer)
			self.inputField = wx.TextCtrl(self, -1, "", size=(500,-1))
			self.sizer.Add(self.inputField)
			self.inputField.Bind(wx.EVT_CHAR, self.OnKeyPress)
		evt.Skip()
	def getSelectedIDs(self):
		"""Gets the database ID's of selected Items."""
		self.subjectlist = []
		modelpanel = self.GetGrandParent().GetParent().mainpanel
		if 1 <= modelpanel.thumbs.GetSelectedItemCount():
			listid = modelpanel.thumbs.GetFirstSelected()
			self.subjectlist.append(modelpanel.thumbs.idFromIndex(listid))
			while listid != -1:
				listid = modelpanel.thumbs.GetNextSelected(listid)
				if listid != -1:
					self.subjectlist.append(modelpanel.thumbs.idFromIndex(listid))

	def OnKeyPress(self, event):
		"""Reads Escape and Return to decide whether to submit the text to the parser or remove the text."""
		## \todo This area is probably a good area to apply Humane interace pseudo modes to.
		val = event.GetKeyCode()
		if wx.WXK_ESCAPE == val:
			self.GetParent().Show(False)
		elif wx.WXK_RETURN == val:
			command, objectslist =  eval(self.inputField.GetValue())
			objects = []
			for each in objectslist:
				objects.append(each[0])
			if command =='tag':

				for id in self.selected:
					models = Model.selectBy(id=id)
					for model in models:
						model.setTags(objects)
			elif command == 'find':
				evt = TagSelectEvent(dmEVT_TAG_SELECT, self.GetId())
				evt.SetTagName(objects[0])
				self.GetEventHandler().ProcessEvent(evt)

				
			self.inputField.Clear()
			#self.GetParent().Show(False)
		else:
			pass
		event.Skip()


class xcommandPanel(wx.Panel):
	"""The command line control """
	def __init__(self, parent, id, size):
		"""Constructor adds a TextCtrl and Binds OnKeyPress."""
		wx.Panel.__init__(self, parent, id, size = size)
		self.sizer = wx.BoxSizer(wx.HORIZONTAL)
		self.SetSizer(self.sizer)
		self.inputField = wx.TextCtrl(self, -1, "", size=(500,-1))
		self.sizer.Add(self.inputField)
		self.inputField.Bind(wx.EVT_CHAR, self.OnKeyPress)
	def getSelectedIDs(self):
		"""Gets the database ID's of selected Items."""
		self.subjectlist = []
		modelpanel = self.GetGrandParent().GetParent().mainpanel
		if 1 <= modelpanel.thumbs.GetSelectedItemCount():
			listid = modelpanel.thumbs.GetFirstSelected()
			self.subjectlist.append(modelpanel.thumbs.idFromIndex(listid))
			while listid != -1:
				listid = modelpanel.thumbs.GetNextSelected(listid)
				if listid != -1:
					self.subjectlist.append(modelpanel.thumbs.idFromIndex(listid))

	def OnKeyPress(self, event):
		"""Reads Escape and Return to decide whether to submit the text to the parser or remove the text."""
		## \todo This area is probably a good area to apply Humane interace pseudo modes to.
		val = event.GetKeyCode()
		if wx.WXK_ESCAPE == val:
			self.GetParent().Show(False)
		elif wx.WXK_RETURN == val:
			command, objectslist =  eval(self.inputField.GetValue())
			objects = []
			for each in objectslist:
				objects.append(each[0])
			if command =='tag':
				self.getSelectedIDs()

				for id in self.subjectlist:
					models = Model.selectBy(id=id)
					for model in models:
						model.setTags(objects)
			elif command == 'find':
				if 0 == len(objects):
					models = Model.select()
				else:
					tagset =Tag.selectBy(tagname=objects[0])
					if 0 != tagset.count():
						tag = tagset.getOne()
						models = tag.models
					else: 
						print "Not Tag by that name"
						models = Model.select()

				self.GetGrandParent().GetParent().mainpanel.update(models)

				
			self.inputField.Clear()
			#self.GetParent().Show(False)
		else:
			pass
		event.Skip()


class controlPanel(wx.Panel):
	""" A panel containing the Command line control """
	def __init__(self, parent, id, size):
		""" Constructor."""
		wx.Panel.__init__(self, parent, id, size = size)
		self.commandPanel = commandPanel(self, -1,self.GetSize()) 
		self.tagPanel = tagCloudPanel(self, -1, (300,150))
		self.sizer = wx.BoxSizer(wx.VERTICAL)
		self.SetSizer(self.sizer)
		self.sizer.Add(self.commandPanel)
		self.sizer.Add(self.tagPanel)


class CommandFrame(wx.MiniFrame):
	""" A miniframe/secondary window for the control Panel."""
	## Currently no used.
	def __init__(self, parent):
		"""Constructor."""
		wx.MiniFrame.__init__(self, parent, -1,"", pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE)
		self.commandPanel = commandPanel(self, -1,self.GetSize())
		self.sizer = wx.BoxSizer(wx.HORIZONTAL)
		self.SetSizer(self.sizer)
		self.sizer.Add(self.commandPanel)

