import sys
import unittest

import posertypes

class TagParserTest(unittest.TestCase):
	def testInit(self):
		testTagParser = posertypes.TagParser()
		self.assertFalse(testTagParser.dropSingletons)
		self.assertTrue(len(testTagParser.ignoreWords) == 0)
		del testTagParser

		testTagParser = posertypes.TagParser(dropSingletons = True)
		self.assertTrue(testTagParser.dropSingletons)
		del testTagParser

		testTagParser = posertypes.TagParser(ignoreWords = ['the', 'and'])
		self.assertTrue(len(testTagParser.ignoreWords) == 2)
		del testTagParser

	def testCallBack(self):
		samples = "This is a test of the parser. The call_back checks for words to skip.".split()
		testTagParser = posertypes.TagParser()
		for word in samples:
			testTagParser.cbTag(word)
		self.assertEquals(len(testTagParser.tags), len(samples))
		del testTagParser

		testTagParser = posertypes.TagParser(dropSingletons = True)
		for word in samples:
			testTagParser.cbTag(word)
		self.assertEquals(len(testTagParser.tags), len(samples) -1)
		del testTagParser

		testTagParser = posertypes.TagParser(ignoreWords = ['the', 'and'], dropSingletons=True)
		for word in samples:
			testTagParser.cbTag(word)
		self.assertEquals(len(testTagParser.tags), len(samples) -3, testTagParser.tags)
		del testTagParser




loadTestCase = unittest.defaultTestLoader.loadTestsFromTestCase 
test_suite = unittest.TestSuite()
test_suite.addTests(loadTestCase(TagParserTest))

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

