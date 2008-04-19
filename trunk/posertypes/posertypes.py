"""
Poser types is a representation of the poser files in python.	

	@Author: Peter Tiegs
	Nascentia Corporation 2007 (Some Rights Reserved).
"""
	
import os
import re
from ZestyParser import *

## Dictionary map between extention and text for type
POSERTYPES = {u".cr2": u"Poser Character",
		  u".pp2":u"Poser Prop",
		  u".pz2":u"Poser Pose",
		  u".hr2":u"Poser Hair",
		  u".hd2":u"Poser Hands",
		  u".lt2":u"Poser LightSet"}
class RuntimePathParser(object):
	"""Parses the path for poser files for data about the model."""
	def __init__(self):
		"""Contstructor sets up the parse tokens."""
		self.runtimefound = False
		tDir = Defer(lambda: self.Dir)
		pathsep = RE(r'[\\\\|\/]')
		dirname = RE(r'[\w\s]+', group=0,callback=self.cbDirname)
		rtdirname = RE(r'[\w\s]+', group=0)
		filename =RE(r'[\w\s]+\.[\w]+',group=0)
		rtDir = TokenSequence( (rtdirname,Omit(pathsep), Omit(RE(r'[Rr]untime')+pathsep+RE(r'[Ll]ibraries')+pathsep+dirname)), callback=self.cbRuntimeFound)
		self.Dir = Omit(pathsep)+(rtDir|dirname) + (tDir|Omit(pathsep)+filename)

	def cbRuntimeFound(self,data):
		"""Callback when the runtime is found.
			@data: the matching string
		"""
		if not self.runtimefound:
			self.pathmeta['runtime'] = data[0]
			self.runtimefound = True

	def cbDirname(self,data):
		"""Callback when a directory is found.
			@data: the matching string (directory name)
		"""
		if self.runtimefound: 
			self.pathmeta['libs'].append(data)

	def getTags(self, liblist):
		"""Given a list of strings parses out tags from only alpha-numeric characters
		to use as meta data tags for the Poser object.
			@liblist: a list of strings (directory names)
		"""
		tags = TokenSeries(RE(r'([a-z]|[^_\-!\s])+', group=0))
		tagset = tags
		retval = []
		for lib in liblist:
			parser = ZestyParser(lib.lower())
			retval= retval+ parser.scan(tagset)
		print retval
		return retval

	def parsePath(self,pathstring):
		"""Parses a directory string with the tokens setup in the constructor.
			@pathstring: full path of a directory containing a poser file type."""
		self.pathmeta = {'runtime':'','libs':[]}
		parser = ZestyParser(pathstring)
		parser.scan(self.Dir)
		liblist = self.pathmeta['libs']
		self.pathmeta['tags']=self.getTags(self.pathmeta['libs'])
		return self.pathmeta

class posertype(object):
	""" This is the base class for all the poser types """
	
	def read(self, filename):
		"""Open and read the Poser file.
			@filename: full path to poser file."""
		self.filename= filename
		base, ext = os.path.splitext(self.filename)
		self.thumb = base+(".png")
		self.type = POSERTYPES[ext]
		input = open(self.filename, "r")
		self.raw = input.readlines()
		input.close()
	def getPathMeta(self):
		"""Parse the directory containing the poser file for additional meta data."""
		return RuntimePathParser().parsePath(os.path.dirname(self.filename))
	def _get_PathMeta(self):
		"""@deprecated: This returns the Meta Data Extracted from the File Path """
		pattern = re.compile('(?:^\/(?:(?:(?:[Rr]untime\/[Ll]ibraries\/[\w\s]+\/)(.*))|([\w\s]+)\/)+)')
		## Need to support windows directory structure	

		if self.filename is not None:
			result = pattern.match(str(self.filename))
			lib, runtime = result.groups()
			libs = os.path.dirname(str(lib)).split('/')
			newlibs = []
			for lib in libs:
				newlib = lib
				if len(newlib) > 0:
					newlibs.append(newlib)	
			libs = newlibs
			retval ={'runtime':runtime}
			for each in libs:
				retval['libs']= libs
		else:
			retval = {}
		return retval

	def parse(self):
		"""Parse the Actual structure of the Poser file."""
		pass
		


