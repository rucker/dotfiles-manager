#!/usr/bin/python

import sys
import os
import shutil
import unittest
import mock

sys.path.insert(0, sys.path[0][:sys.path[0].rfind('test')])

import env
import testenv
import dotfilesmanager
import testfilemocks
import gitconfig
from constants import Srcfiles, Dotfiles

class GitConfigIntTest(unittest.TestCase):

    def setUp(self):
        dotfilesmanager.init()
        testenv.setUp()

    def tearDown(self):
        testenv.clearArgs()
        testenv.tearDown()

    def testWhenUserPassesArg_no_localGitConfigOutputFileContainsContentsOfGitConfigButNotGitLocal(self):
        env.args = env.parser.parse_args(['--no-local'])
        gitconfig.compileGitConfig()
        with open(env.outputFilesDir + Dotfiles.GITCONFIG.value) as dotGitConfig:
            with open(env.inputFilesDir + Srcfiles.GITCONFIG.value) as gitConfig:
                with open(env.inputFilesDir + Srcfiles.GITCONFIG_LOCAL.value) as gitLocal:
                    contents = dotGitConfig.read()
                    self.assertTrue(gitConfig.read() in contents)
                    self.assertTrue(gitLocal.read() not in contents)

    def testGitConfigOutputFileContainsTheContentsOfGitConfigAndGitLocal(self):
        gitconfig.compileGitConfig()
        with open(env.homeDir + Dotfiles.GITCONFIG.value) as dotGitConfig:
            with open(env.inputFilesDir + Srcfiles.GITCONFIG.value) as gitConfig:
                with open(env.inputFilesDir + Srcfiles.GITCONFIG_LOCAL.value) as gitLocal:
                    contents = dotGitConfig.read()
                    self.assertTrue(gitConfig.read() in contents)
                    self.assertTrue(gitLocal.read() in contents)

suite = unittest.TestLoader().loadTestsFromTestCase(GitConfigIntTest)
unittest.main(module=__name__, buffer=True, exit=False)
