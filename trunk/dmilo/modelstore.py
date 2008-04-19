from sqlobject import SQLObject, UnicodeCol,StringCol,EnumCol, RelatedJoin, connectionForURI, sqlhub
import sys
import os
class Model(SQLObject):
	"""Columns for 3D Model metadata"""
	## Locaton of thumbnail on Disk
	thumb = UnicodeCol()
	## Location of Readme file on Disk
	readme= UnicodeCol()
	## Location fo 3d model file on Disk
	filename= UnicodeCol(alternateID=True)
	## Type of file Could be (Mime-type, extention, or User understood type)
	## currently only User understood type
	type= UnicodeCol()
	## Dublin core Creater name
	creator=UnicodeCol()
	## Creative commons description of License
	license = UnicodeCol()
	## Set of tags Associated with this 3d Model
	tags = RelatedJoin('Tag')
	## Collections containing this model.
	collections = RelatedJoin('Collection')
	
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
			tagname = tagname.lower()
			subtags=  tagname.split(' ')
			if 1 < len(subtags):
				self.setTags(subtags)
			else:
				tagset = Tag.selectBy(tagname=tagname)
				if 0 == tagset.count():
					newtag = Tag(tagname=tagname)
				else:
					newtag = tagset.getOne()
				self.addTag(newtag)

class Tag(SQLObject):
	"""Table for Tags or Keywords."""
	## The Tag text
	tagname = StringCol(alternateID=True)
	## The Type of Tag @deprecated
	tagtype = EnumCol(enumValues = ['User', 'Auto'], default='User')
	## Models that have been tagged with this keyword.
	models = RelatedJoin('Model')

class Collection(SQLObject):
	""" Table for Collections."""
	## The Name of the Collection or Set
	setname = StringCol(alternateID=True)
	## Models that are in the Set
	models= RelatedJoin('Model')

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
		sqlhub.processConnection = connectionForURI('sqlite:'+self.dbfile)

	def newStore(self, dbfile="models.db"):
		"""Create a new Database
			@dbfile: path the database
		"""
		Model.createTable()
		Tag.createTable()
		Collection.createTable()
	
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


	
