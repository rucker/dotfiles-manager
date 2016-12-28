#!/usr/bin/python

import unittest
import tempfile
import sys
import os
import mock

sys.path.insert(0, sys.path[0][:sys.path[0].rfind('test')])

import testenv
import methodstubs

class TestEnvTest(unittest.TestCase):

    @mock.patch('shutil.rmtree')
    def testWhenTestEnvContainsRealDirectoryNamesTearDownWillExitWithStatus1(self, rmtree):
        rmtree.side_effect = methodstubs.noop(self)
        with self.assertRaises(SystemExit) as se:
            testenv.tmp = tempfile.gettempdir()
            testenv.outputDir = 'foo/bar'
            testenv.tearDown()
        self.assertEqual(se.exception.code, 1)

    @mock.patch('os.remove')
    def testWhenTestEnvContainsRealConfigFileNameTearDownWillExitWithStatus1(self, rm):
        rm.side_effect = methodstubs.noop(self)
        with self.assertRaises(SystemExit) as se:
            testenv.tmp = tempfile.gettempdir()
            testenv.configFile = 'foobar'
            testenv.tearDown()
        self.assertEqual(se.exception.code, 1)

suite = unittest.TestLoader().loadTestsFromTestCase(TestEnvTest)
unittest.main(module=__name__, buffer=True, exit=False)
