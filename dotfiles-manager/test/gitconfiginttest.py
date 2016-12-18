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
from constants import GitConfigInputFiles, GitConfigOutputFiles

class GitConfigIntTest(unittest.TestCase):

    def setUp(self):
        dotfilesmanager.init()
        testenv.setUp()

    def tearDown(self):
        testenv.tearDown()

    def testWhenGitConfigFileIsWrittenItContainsTheContentsOfGitPublicButNotGitLocal(self):
        gitconfig.compileGitConfig()
        with open(env.outputFilesDir + GitConfigOutputFiles.GITCONFIG.value) as dotGitConfig:
            with open(env.inputFilesDir + GitConfigInputFiles.GIT_PUBLIC.value) as gitPublic:
                with open(env.inputFilesDir + GitConfigInputFiles.GIT_LOCAL.value) as gitLocal:
                    contents = dotGitConfig.read()
                    self.assertTrue(gitPublic.read() in contents)
                    self.assertTrue(gitLocal.read() not in contents)

    def testWhenGitConfigDotFileIsWrittenItContainsTheContentsOfGitPublicAndGitLocal(self):
        gitconfig.compileGitConfig()
        with open(env.homeDir + GitConfigOutputFiles.DOT_GITCONFIG.value) as dotGitConfig:
            with open(env.inputFilesDir + GitConfigInputFiles.GIT_PUBLIC.value) as gitPublic:
                with open(env.inputFilesDir + GitConfigInputFiles.GIT_LOCAL.value) as gitLocal:
                    contents = dotGitConfig.read()
                    self.assertTrue(gitPublic.read() in contents)
                    self.assertTrue(gitLocal.read() in contents)

suite = unittest.TestLoader().loadTestsFromTestCase(GitConfigIntTest)
unittest.main(module=__name__, buffer=True, exit=False)
