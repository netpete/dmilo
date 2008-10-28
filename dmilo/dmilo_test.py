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

class TagSQLTest(unittest.TestCase):
	def testAddTag(self):
		modelstore.Tag.createTable(ifNotExists=True)
		modelstore.Tag(tagname= 'New')
		actualTag = modelstore.Tag.get(1)
		self.assertTrue('New' == actualTag.tagname)
		modelstore.Tag.dropTable(ifExists=True)

class CollectionSQLTest(unittest.TestCase):
	def setUp(self):
		createDB()
	def testAddCollection(self):
		modelstore.Collection.createTable(ifNotExists=True)
		modelstore.Collection(setname= 'New')
		actualCollection = modelstore.Collection.get(1)
		self.assertTrue('New' == actualCollection.setname)
		modelstore.Collection.dropTable(ifExists=True)
		
class VirtualDir_CatalogSQLTest(unittest.TestCase):
	realPath = '/path/to/thing'
	def setUp(self):
		modelstore.VirtualDir.createTable()
		modelstore.Catalog.createTable()
	def tearDown(self):
		modelstore.Catalog.dropTable()
		modelstore.VirtualDir.dropTable()

	def testAddVirtualDir(self):
		newCatalog = modelstore.Catalog()
		modelstore.VirtualDir(fullpath = self.realPath, dirname='thing', root=False, catalogID=newCatalog)
		actualVDir = modelstore.VirtualDir.get(1)
		self.assertTrue(actualVDir.fullpath == self.realPath)
	
	def testGetAllSubdirs(self):
		thingDir = modelstore.VirtualDir(fullpath = self.realPath, dirname='thing', root=False, catalogID=modelstore.Catalog())
		toCatalog = modelstore.Catalog()
		toCatalog.addVirtualDir(thingDir)
		toDir = modelstore.VirtualDir(fullpath = os.path.dirname(self.realPath), dirname='to', root=False, catalogID=toCatalog)
		self.assertTrue(modelstore.VirtualDir.selectBy(id = toDir.getAllSubdirs()[0])[0].fullpath == self.realPath)	
		self.assertTrue(len(thingDir.getAllSubdirs())== 0)	

class ThumbnailSQLTest(unittest.TestCase):
	def setUp(self):
		modelstore.Thumbnail.createTable(ifNotExists=True)

	def testAddThumbnail(self):
		thumbFile = 'this.png'
		thumbData = 'someblockofbinarydata'
		modelstore.Thumbnail(filename=thumbFile, bitmap=thumbData, width=1, height=1)
		self.assertTrue(modelstore.Thumbnail.get(1).filename == thumbFile)
	def tearDown(self):
		modelstore.Thumbnail.dropTable(ifExists=True)
		
class ModelStoreTest(unittest.TestCase):
	
	def testInitNoDB(self):
		newStore = modelstore.ModelStore()
		expectedDB = os.path.join(os.getcwd(),'models1.db')
		self.assertTrue(newStore.dbfile== expectedDB, "newStore.dbfile = %s, expected is %s")
		self.assertFalse(os.path.exists(expectedDB))

	def testInitDB(self):
		expectedDB = os.path.join(os.getcwd(),'testDB.db')
		newStore = modelstore.ModelStore(expectedDB)
		self.assertTrue(newStore.dbfile== expectedDB, "newStore.dbfile = %s, expected is %s"%(newStore.dbfile, expectedDB))
		self.assertFalse(os.path.exists(expectedDB))

	def testNewStore(self):
		expectedDB = os.path.join(os.getcwd(),'testDB.db')
		newStore = modelstore.ModelStore(expectedDB)
		newStore.newStore()
		self.assertTrue(newStore.dbfile== expectedDB, "newStore.dbfile = %s, expected is %s"%(newStore.dbfile, expectedDB))
		self.assertTrue(os.path.exists(expectedDB))
		os.unlink(expectedDB)

				

test_suite = unittest.TestSuite()
test_suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(ModelSQLTest))
test_suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(TagSQLTest))
test_suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(CollectionSQLTest))
test_suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(VirtualDir_CatalogSQLTest))
test_suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(ThumbnailSQLTest))
test_suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(ModelStoreTest))

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

