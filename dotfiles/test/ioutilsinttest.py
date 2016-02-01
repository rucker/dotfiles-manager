#!/usr/bin/python

import unittest
import sys

sys.path.insert(0, sys.path[0][:sys.path[0].rfind('test')])

import env
import testenv
import ioutils
from constants import BashInputFiles, BashOutputFiles

class IOUtilsIntTest(unittest.TestCase):
  
  @classmethod
  def setUpClass(self):
    testenv.setUp()

  @classmethod
  def tearDownClass(self):
    testenv.tearDown()

  def testMapInputFileContentsMapsAKeyValuePair(self):
    map = dict()
    ioutils.mapInputFileContents(BashInputFiles.BASH_COMMON.value, map)
    with open(env.inputFilesDir + BashInputFiles.BASH_COMMON.value) as bashCommon:
      lines = bashCommon.readlines()
      self.assertTrue(len(lines) == len(map))
      for line in lines:
        pair = line.split('=')
        self.assertTrue(map[pair[0]] == pair[1])
  
  def testMapInputFileContentsSkipsFunctions(self):
    with open(env.inputFilesDir + 'test_file', 'w') as bashCommon:
      bashCommon.write('function foo() {}\n')
      bashCommon.write('bar=baz')

    map = dict()
    ioutils.mapInputFileContents('test_file', map)

    self.assertTrue(len(map) == 1)
    self.assertTrue(map.has_key('bar'))
    self.assertTrue(map['bar'] == 'baz')

  def testWriteOutputFileWritesMapToFile(self):
    map = dict()
    ioutils.mapInputFileContents(BashInputFiles.BASH_COMMON.value, map)
    ioutils.writeOutputFile(env.outputFilesDir + BashOutputFiles.BASH_PROFILE.value, map)
    with open(env.inputFilesDir + BashInputFiles.BASH_COMMON.value) as bashCommon:
      with open(env.outputFilesDir + BashOutputFiles.BASH_PROFILE.value) as bashProfile:
	self.assertTrue(set(bashCommon.readlines()) == set(bashProfile.readlines()))

suite = unittest.TestLoader().loadTestsFromTestCase(IOUtilsIntTest)
unittest.main(module=__name__, buffer=True, exit=False)
