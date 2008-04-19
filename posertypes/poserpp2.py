
__author__='Peter Tiegs'
"""
	Poser Prop Module	

	@Author: %s
	Nascentia Corporation 2007 (Some Rights Reserved).
	"""%(__author__)
	
from posertypes import posertype
class poserpp2(posertype):
	"""Poser prop class"""
	def parse(self):
		"""Parses the internals of the poser prop file type."""
		for line in self.raw:
			if line.find("version") != -1:
				head = self.raw.index(line)
				self.version = self.raw[head +2]
			elif line.find("objFileGeom") != -1:
				print line
				self.res = line

			# Are there any other files
			#elif line.find(".") != -1:
			#	print line
