"""
	Functions to import Assets into the dMilo Database.	

	@Author: Peter Tiegs
	Nascentia Corporation 2007 (Some Rights Reserved).
	"""
	
__author__="Peter Tiegs"
import sys
import os
from posertypes import POSERTYPES, posertype
from modelstore import Model, ModelStore
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
		thismodel = Model(filename = item.filename, thumb= item.thumb, type=item.type, readme="", creator="Unknown", license="Unknown")
		## Generates the autotags based on path.
		if autotags:
			pathmeta = item.getPathMeta()
			if pathmeta.has_key('runtime'):
				thismodel.setTags([pathmeta['runtime']]) # setTags takes a list not a string
			if pathmeta.has_key('tags'):
				thismodel.setTags(pathmeta['tags'])
			thismodel.setTags(item.type.split())
	else:
		pass
		#print "Allready there%s"%item.filename

def scandir(directory):
	"""Scan a directory for items to import.
		@directory: Path to items."""
	#print directory
	for each in os.listdir(directory):
		if os.path.isdir(os.path.join(directory,each)):	
			scandir(os.path.join(directory,each))
		else:
			if each.startswith("._"):
				pass #print each
			else:
				ext = os.path.splitext(each)[1]
				if ext in POSERTYPES.keys():
					item = posertype()
					item.read(os.path.join(directory, each))
					importItem(item)


def main(directory):
	""" Run the database import as a seperate process. """
	db=ModelStore()
	scandir(directory)


if __name__=="__main__":
	main(sys.argv[1])
