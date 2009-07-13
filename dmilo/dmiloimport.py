"""
	Functions to import Assets into the dMilo Database.	

	@Author: Peter Tiegs
	Nascentia Corporation 2007 (Some Rights Reserved).
	"""
	
__author__="Peter Tiegs"
import sys
import os
import time
import hashlib
from unittest import TestCase
import pkg_resources
import wx
from posertypes import POSERTYPES, posertype, parsePath 
from modelstore import Thumbnail, Model,VirtualDir,Catalog, ModelStore
#from rsrconvert import rsr2png


def importItem( item, autotags=True, resetRSR=True, shadow=None):
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
	dbcount = Model.select(Model.q.filename==item.filename).count()
	if 0 == dbcount :
		if os.path.exists(item.thumb):
			image = wx.Image(item.thumb, wx.BITMAP_TYPE_PNG)
			if image.IsOk():
				thumb = Thumbnail(filename=item.thumb, bitmap=image.GetData(), width=image.GetWidth(), height=image.GetHeight())
			else:
				thumb = Thumbnail.selectBy(filename=pkg_resources.resource_filename('dmilo', 'resource/nothumb.png'))[0]
		else:
			thumb = Thumbnail.selectBy(filename=pkg_resources.resource_filename('dmilo', 'resource/nothumb.png'))[0]
		thismodel = Model(filename = item.filename, chksum = item.chksum, thumb= thumb, type=item.type, readme="", creator="Unknown", license="Unknown")
		## Generates the autotags based on path.
		if autotags:
			pathmeta = item.getPathMeta()
			if pathmeta.has_key('runtime'):
				#thismodel.setTags([pathmeta['runtime']]) # setTags takes a list not a string
				thismodel.addToCollection(pathmeta['runtime'])
			if pathmeta.has_key('tags'):
				thismodel.setTags(pathmeta['tags'], shadow=shadow)
			thismodel.addToCollection(item.type)
			vDirs = [pathmeta['runtime'], item.type]
			vDirs.extend(pathmeta['libs'])
	
			vDirs.reverse() # so stack is in correct order
	
		wx.LogDebug("Added to Database %s"%(item.filename))
		return thismodel
	else:
		wx.LogDebug( "Already in Database %s"%item.filename)
		return None

dotDmiloPath =  os.path.join(os.path.expanduser('~'), '.dmilo')

def scandir(directory):
	"""Scan a directory for items to import.
		@directory: Path to items."""
	ms = ModelStore(os.path.join(dotDmiloPath, 'dmilo.db') )
	mr = ms.shadow.getroot().find('Models')
	dr = ms.shadow.getroot().find('Directories')
	for root, dirs, files in os.walk( directory ):
		pathMeta =  parsePath( root )
		if pathMeta['runtime']:
			topDir =  len( pathMeta['libs']) == 0
			currentSet = VirtualDir.selectBy(fullpath=root)
			if 0 == currentSet.count():
				cat = Catalog()
				if topDir:
					basename = pathMeta['runtime']
				else:
					basename = os.path.basename(root)
				dirid = u'.'.join( dirs+files ).encode("utf-8")
				chksum = hashlib.md5(dirid).hexdigest()
				currentDir = VirtualDir(dirname = basename, fullpath = root, chksum = chksum, catalogID=cat, root = topDir)
				dr.append( currentDir.asElement() )
				if not topDir:
					parent = list( VirtualDir.selectBy(fullpath = os.path.dirname(root) ))
					if len (parent):
						parent[0].catalog.addVirtualDir( currentDir )
					else:
						wx.LogError( "ERROR Child dir exists before parent")

			else:
				currentDir = currentSet[0]	
			for each in files:
				if each.startswith("._"):
					pass 
				else:
					ext = os.path.splitext(each)[1]
					if ext in POSERTYPES.keys():
						item = posertype()
						item.read(os.path.join(root, each))
						newModel = importItem(item, shadow=(mr, ms.shadowFilename()))
						if newModel is not None:
							mr.append( newModel.asElement() )
							currentDir.addModel(newModel)

	wx.LogDebug(" Writing xml")
	ms.shadow.write( ms.shadowFilename() )
	wx.LogDebug("done")
							
			

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


