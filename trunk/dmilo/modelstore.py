#!/usr/bin/python
import sys
import os

import sqlobject
import pkg_resources
import wx
import rdflib

class Model(sqlobject.SQLObject):
	"""Columns for 3D Model metadata"""
	thumb = sqlobject.ForeignKey('Thumbnail')
	#: Location of Readme file on Disk
	readme= sqlobject.UnicodeCol()
	#: Location fo 3d model file on Disk
	filename= sqlobject.UnicodeCol(alternateID=True)
	#: Type of file Could be (Mime-type, extention, or User understood type)
	#: currently only User understood type
	type= sqlobject.UnicodeCol()
	#: Dublin core Creater name
	creator=sqlobject.UnicodeCol()
	#: Creative commons description of License
	license = sqlobject.UnicodeCol()

	#: Set of tags Associated with this 3d Model
	tags = sqlobject.RelatedJoin('Tag')

	#: Collections containing this model.
	collections = sqlobject.RelatedJoin('Collection')
	virtualDir = sqlobject.RelatedJoin('VirtualDir')

	
	def _get_name(self):
		"""Name of the model  Currently filename."""
		return os.path.basename(self.filename)
	def _get_title(self):
		"""Returns the name in xml formated syntax."""
		pass	

	def _get_lib(self):
		""" Directory containing the model"""
		return os.path.basename(os.path.dirname(self.filename))

	def setTags(self, taglist):
		"""Tag list is a list of tag strings"""
		for tagname in taglist:
			if tagname:
				tagname = tagname.lower()
				subtags=  tagname.split()
				if 1 < len(subtags):
					self.setTags(subtags)
				else:
					tagset = Tag.selectBy(tagname=tagname)
					if 0 == tagset.count():
						newtag = Tag(tagname=tagname)
					else:
						newtag = tagset.getOne()
					if newtag not in self.tags:
						self.addTag(newtag)
	
	def addToCollection(self, name):
		setname = name
		collectionSet =Collection.selectBy(setname=setname)
		if 0 == collectionSet.count():
			collectionEntry = Collection(setname=setname)
		else:
			collectionEntry =collectionSet.getOne()
		self.addCollection(collectionEntry)

class Tag(sqlobject.SQLObject):
	"""Table for Tags or Keywords."""
	## The Tag text
	tagname = sqlobject.StringCol(alternateID=True)
	## The Type of Tag @deprecated
	tagtype = sqlobject.EnumCol(enumValues = ['User', 'Auto'], default='User')
	## Models that have been tagged with this keyword.
	models = sqlobject.RelatedJoin('Model')

class Collection(sqlobject.SQLObject):
	""" Table for Collections."""
	## The Name of the Collection or Set
	setname = sqlobject.StringCol(alternateID=True)
	## Models that are in the Set
	models= sqlobject.RelatedJoin('Model')

class Catalog(sqlobject.SQLObject):
	parent = sqlobject.MultipleJoin('VirtualDir')
	subdirs = sqlobject.RelatedJoin('VirtualDir')

class VirtualDir(sqlobject.SQLObject):
	dirname = sqlobject.StringCol()
	root = sqlobject.BoolCol()
	fullpath = sqlobject.StringCol(alternateID=True)
	models = sqlobject.RelatedJoin('Model')
	catalog = sqlobject.ForeignKey('Catalog')
	pc = sqlobject.RelatedJoin('Catalog')
	def getAllSubdirs(self):
		retval =[]
		for x in self.catalog.subdirs:
			retval.append(x.id)
			retval.extend(x.getAllSubdirs())
		return retval

class Thumbnail(sqlobject.SQLObject):
	## Locaton of thumbnail on Disk
	filename = sqlobject.UnicodeCol(alternateID=True)
	## Bitmap data
	bitmap = sqlobject.BLOBCol()
	width = sqlobject.IntCol()
	height = sqlobject.IntCol()

	

class ModelStore(object):
	"""Class with functions to Connect to a Database and Create a new one."""
	## Path to Database
	dbfile = ''
	def __init__(self, dbfile="models1.db"):
		"""Connect to Database
			@dbfile: path the database
		"""
		if os.name=="nt":
			parts=  os.path.abspath(dbfile).split('\\')
			parts[0]= '|'.join(parts[0].split(':'))
			self.dbfile= '/'+'/'.join(parts)
			#sys.exit()
		else:
			self.dbfile = os.path.abspath(dbfile)
		sqlobject.sqlhub.processConnection = sqlobject.connectionForURI('sqlite:'+self.dbfile)

	def newStore(self):
		"""Create a new Database
		"""
		Thumbnail.createTable()
		# add default thumbnails
		nothumbfile = pkg_resources.resource_filename('dmilo', 'resource/nothumb.png')
		nothumbimage = wx.Image(nothumbfile, wx.BITMAP_TYPE_PNG)
		Thumbnail(filename=nothumbfile, bitmap=nothumbimage.GetData(), width=nothumbimage.GetWidth(), height=nothumbimage.GetHeight()) 
		Model.createTable()
		Tag.createTable()
		Collection.createTable()
		VirtualDir.createTable()
		Catalog.createTable()

	def serialize(self, outfile='outfile.xml'):
		rGraph = rdflib.Graph()
	
		

	
if __name__=="__main__":
	print "TestCode"
	testdb = os.path.abspath(os.path.join(os.getcwd(),'models.db'))
	#testdb ='/c|/models.db'
	if sys.argv[1] == '-n':
		if os.path.exists(testdb):
			os.unlink(testdb)
		print "New DB"
	dbfile=os.path.join(os.getcwd(),testdb)
	db =ModelStore(dbfile)
	if sys.argv[1] == '-n':
		db.newStore()


	
