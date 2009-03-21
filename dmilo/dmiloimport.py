"""
	Functions to import Assets into the dMilo Database.	

	@Author: Peter Tiegs
	Nascentia Corporation 2007 (Some Rights Reserved).
	"""
	
__author__="Peter Tiegs"
import sys
import os
from unittest import TestCase
import pkg_resources
import wx
from posertypes import POSERTYPES, posertype
from modelstore import Thumbnail, Model,VirtualDir,Catalog, ModelStore
#from rsrconvert import rsr2png


def importItem( item, autotags=True, resetRSR=True):
	""" import and item into the Database. 
		@item: a posertype ."""
	if resetRSR:
		rsr =  os.path.splitext(item.thumb)[0]+'.rsr'
		if os.path.exists(rsr):
			try:
				rsr2png(rsr)
			except:
				pass
	## adds Model to the Database.
	if 0 == Model.select(Model.q.filename==item.filename).count():
		if os.path.exists(item.thumb):
			image = wx.Image(item.thumb, wx.BITMAP_TYPE_PNG)
			if image.IsOk():
				thumb = Thumbnail(filename=item.thumb, bitmap=image.GetData(), width=image.GetWidth(), height=image.GetHeight())
			else:
				thumb = Thumbnail.selectBy(filename=pkg_resources.resource_filename('dmilo', 'resource/nothumb.png'))[0]
		else:
			thumb = Thumbnail.selectBy(filename=pkg_resources.resource_filename('dmilo', 'resource/nothumb.png'))[0]
		thismodel = Model(filename = item.filename, thumb= thumb, type=item.type, readme="", creator="Unknown", license="Unknown")
		
		## Generates the autotags based on path.
		if autotags:
			pathmeta = item.getPathMeta()
			if pathmeta.has_key('runtime'):
				#thismodel.setTags([pathmeta['runtime']]) # setTags takes a list not a string
				thismodel.addToCollection(pathmeta['runtime'])
			if pathmeta.has_key('tags'):
				thismodel.setTags(pathmeta['tags'])
			thismodel.addToCollection(item.type)
			vDirs = [pathmeta['runtime'], item.type]
			vDirs.extend(pathmeta['libs'])
	
			vDirs.reverse() # so stack is in correct order
	
			addDirs(vDirs, thismodel)
		wx.LogDebug("Added to Database %s"%(item.filename))
	else:
		wx.LogDebug( "Already in Database %s"%item.filename)

def addDirs(dirStack, model, parDir=''):
	if len (dirStack) >0:
		
		currentName = dirStack.pop()
		if parDir:
			fullPath=os.path.join(parDir, currentName)
			topDir =False
		else:
			fullPath=currentName
			topDir =True
		currentSet = VirtualDir.selectBy(fullpath=fullPath)
		if 0 == currentSet.count():
			cat = Catalog()
			currentDir=VirtualDir(dirname=currentName, fullpath=fullPath, catalogID=cat.id, root=topDir)
		else:
			currentDir=currentSet.getOne()
			cat = currentDir.catalog

		subDir = addDirs(dirStack, model,  parDir=fullPath)
		if subDir:
			if not subDir in cat.subdirs:
				cat.addVirtualDir(subDir)
		else:
			currentDir.addModel(model)
		retval = currentDir
	else:
		
		retval = None
	return retval

def scandir(directory):
	"""Scan a directory for items to import.
		@directory: Path to items."""
	for each in os.listdir(directory):
		if os.path.isdir(os.path.join(directory,each)):	
			scandir(os.path.join(directory,each))
		else:
			if each.startswith("._"):
				pass 
			else:
				ext = os.path.splitext(each)[1]
				if ext in POSERTYPES.keys():
					item = posertype()
					item.read(os.path.join(directory, each))
					importItem(item)

class ImportTest(TestCase):
	def testImportItem(self):
		testItem = posertype()
		testItem.thumb = 'test.png'
		testItem.filename = 'test.file'
		testItem.type = 'testType'
		self.assert_(importItem(testItem, autotags=True, resetRSR=True))

		
	
	

def main(directory, dbPath):
	""" Run the database import as a seperate process. """
	db=ModelStore(dbfile=dbPath)
	scandir(directory)


if __name__=="__main__":
	main(sys.argv[1], sys.argv[2])


