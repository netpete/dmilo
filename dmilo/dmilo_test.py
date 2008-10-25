import sys
import os
import unittest
import modelstore

def createDB():
	from sqlobject import sqlhub, connectionForURI
	connection = connectionForURI('sqlite:/:memory:')
	sqlhub.processConnection = connection
	
class ModelSQLTest(unittest.TestCase):
	testInputA = {
		'inputReadme': 'README',
		'inputFilename' :"/this/path/to/SOMEFILE",
		'inputType' : "Poser type",
		'inputCreator' : "Peter Tiegs",
		'inputLicense' : "MIT",
		'inputThumbID': 1,
	}
	def addModel(self):
		self.assertTrue(0 == modelstore.Model.select().count())
		modelstore.Model(readme = self.testInputA['inputReadme'],
			filename = self.testInputA['inputFilename'],
			type = self.testInputA['inputType'],
			creator = self.testInputA['inputCreator'],
			license = self.testInputA['inputLicense'],
			thumbID = self.testInputA['inputThumbID'])

		self.assertTrue(1 == modelstore.Model.select().count())

	def setUp(self):
		createDB()
		modelstore.Model.createTable(ifNotExists=True)
	def testAddItem(self):
		self.addModel()
		actualItem = modelstore.Model.get(1)
		self.assertTrue(actualItem.filename == self.testInputA['inputFilename'])

	def testGetName(self):
		self.assert_(modelstore.Model.name)
		self.addModel()
		actualItem = modelstore.Model.get(1)
		self.assertTrue('SOMEFILE' == actualItem.name)

	def testGetTitle(self):
		self.assert_(modelstore.Model.title)

	def testGetLib(self):
		self.assert_(modelstore.Model.lib)
		self.addModel()
		actualItem = modelstore.Model.get(1)
		self.assertTrue('to' == actualItem.lib)

	def testSetTags(self):
		self.assert_(modelstore.Model.tags)
		modelstore.Tag.createTable(ifNotExists=True)
		self.addModel()
		actualItem = modelstore.Model.get(1)
		self.assertTrue(0 == len(actualItem.tags))
		
		actualItem.setTags(['Hello'])
		self.assertTrue(1 == len(actualItem.tags))
		actualItem.setTags(['Hello','today'])
		self.assertTrue(2 == len(actualItem.tags), "Length of tags is %d, expected is 2"%(len(actualItem.tags)))
		actualItem.setTags(['test case'])
		self.assertTrue(4 == len(actualItem.tags), "Length of tags is %d, expected is 4"%(len(actualItem.tags)))
		actualItem.setTags([])
		self.assertTrue(4 == len(actualItem.tags), "Length of tags is %d, expected is 4"%(len(actualItem.tags)))
		actualItem.setTags([''])
		self.assertTrue(4 == len(actualItem.tags), "Length of tags is %d, expected is 4"%(len(actualItem.tags)))
		
		modelstore.Tag.dropTable(ifExists=True)

	def testAddToCollection(self):
		modelstore.Collection.createTable(ifNotExists=True)
		modelstore.Collection(setname = 'Favorites')
		self.addModel()
		actualItem = modelstore.Model.get(1)
		self.assertTrue(0 == len(actualItem.collections))
		
		actualItem.addToCollection('Favorites')
		testCollection = modelstore.Collection.selectBy(setname='Favorites')[0]
		self.assertTrue(len(testCollection.models) == 1, "Actual length of Models =%d"%len(testCollection.models)  )
		modelInCollection = testCollection.models[0]
		self.assertTrue(actualItem == modelInCollection, "actualItem %r, ItemInCollection %r"%(actualItem, modelInCollection)  )
		modelstore.Collection.dropTable(ifExists=True)

	def tearDown(self):
		modelstore.Model.dropTable(ifExists=True)

		
		

test_suite = unittest.TestSuite()
test_suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(ModelSQLTest))

def bool2Return(boolVal):
	if boolVal:
		ret= 0
	else:
		ret= 1
	return ret

def main():
	ret = bool2Return(unittest.TextTestRunner().run(test_suite).wasSuccessful())
	return ret 

if __name__ == "__main__":
	sys.exit(main())

