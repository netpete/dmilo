"""
	Poser Characters Module	

	@Author: %s
	Nascentia Corporation 2007 (Some Rights Reserved).
	"""%('Peter Tiegs')
from posertypes import posertype
	
class posercr2(posertype):
	"""Poser Character class."""
	def parse(self):
		"""Parses the internals of the poser character file type."""
		for line in self.raw:
			if line.find("version") != -1:
				head = self.raw.index(line)
				self.version = self.raw[head +2]
			elif line.find("figureResFile") != -1:
				print line
				self.res = line

			# Are there any other files
			#elif line.find(".") != -1:
			#	print line
