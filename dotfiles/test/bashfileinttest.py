#!/usr/bin/python

import sys
import unittest
import io
import os
import __builtin__
from mock import mock_open, patch

sys.path.insert(0, sys.path[0][:sys.path[0].rfind('test')])

import env
import dotfiles
from dotfiles import bashfile
from constants import Systems, BashInputFiles

class BashFileIntTest(unittest.TestCase):

  @classmethod
  def setUpClass(self):
    dotfiles.init()
    env.inputFilesDir = ''
    env.outputFilesDir = ''
    self.createInputFiles()

  @classmethod
  def tearDownClass(self):
    self.destroyInputAndOutputFiles()

  def testBashCommonAndBashMacWrittenToBashProfile(self):
    bashfile.compileBashProfile()
    with open(env.outputFilesDir + 'bash_profile') as bashProfile:
      contents = bashProfile.read()
      with open(env.inputFilesDir + 'bash_common') as bashInput:
        self.assertTrue(bashInput.read() in contents)
      with open(env.inputFilesDir + 'bash_mac') as bashInput:
        self.assertTrue(bashInput.read() in contents)

  def testBashLinuxNotWrittenToBashProfile(self):
    bashfile.compileBashProfile()
    with open(env.outputFilesDir + 'bash_profile') as bashProfile:
      contents = bashProfile.read()
      with open(env.inputFilesDir + 'bash_linux') as bashInput:
        self.assertTrue(bashInput.read() not in contents)

  @classmethod
  def createInputFiles(self):
    with open('bash_common', 'w') as bashCommon:
      bashCommon.write('some_common_token=some_common_value')
    with open('bash_mac', 'w') as bashMac:
      bashMac.write('some_mac_token=some_mac_value')
    with open('bash_linux', 'w') as bashLinux:
      bashLinux.write('some_linux_token=some_linux_value')
    with open('bash_private', 'w') as bashPrivate:
      bashPrivate.write('some_private_token=some_private_value')

  @classmethod
  def destroyInputAndOutputFiles(self):
    for file in ['bash_common', 'bash_mac', 'bash_linux', 'bash_private', 'bash_profile', 'bashrc']:
      if os.path.isfile(file):
        os.remove(file)

suite = unittest.TestLoader().loadTestsFromTestCase(BashFileIntTest)
unittest.main(module=__name__, buffer=True, exit=False)
