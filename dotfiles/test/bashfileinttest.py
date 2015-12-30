#!/usr/bin/python

import sys
sys.path.insert(0, '../')
import unittest
import io
import __builtin__
from mock import mock_open, patch

import env
import dotfiles
from dotfiles import bashfile
from constants import Systems, BashInputFiles

class BashFileIntTest(unittest.TestCase):

  def testBashCommonAndBashMacWrittenToBashProfile(self):
    dotfiles.init()
    bashfile.compileBashProfile()
    with open(env.outputFilesDir + 'bash_profile') as bashProfile:
      contents = bashProfile.read()
      with open(env.inputFilesDir + 'bash_common') as bashCommon:
        self.assertTrue(bashCommon.read() in contents)
      with open(env.inputFilesDir + 'bash_mac') as bashMac:
        self.assertTrue(bashMac.read() in contents)

suite = unittest.TestLoader().loadTestsFromTestCase(BashFileIntTest)
unittest.main(module=__name__, buffer=True, exit=False)
