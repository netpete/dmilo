import os
import sys


class Preference:
	"""Preferences module is currently unused."""
	def __init__(self):
		"""Constructor."""
		if sys.platform =='win32':
			self.prefDir = os.path.join(os.environ['HOMEPATH'], '.dmilo')
		else:
			self.prefDir = os.path.join(os.environ['HOME'], '.dmilo')

		if os.path.exists(self.prefDir):
			self.dbPath = os.path.join(self.prefDir, 'models.db')
			self.resourcePath = os.path.join(self.prefDir, 'resource')
		else:
			self.dbPath = os.path.join(os.path.dirname(__file__), 'models.db')
			self.resourcePath = os.path.join(os.path.dirname(__file__), 'resource')

dmPREF = Preference()
