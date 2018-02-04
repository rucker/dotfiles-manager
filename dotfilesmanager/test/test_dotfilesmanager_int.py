import os
from os.path import join
import shutil
import unittest
from unittest import mock

from dotfilesmanager.test import env
from dotfilesmanager import dfm
from dotfilesmanager import ioutils

class TestDotfilesManagerInt(unittest.TestCase):

    FIRST_INPUT_FILE = '99-fooconfig'
    SECOND_INPUT_FILE = '98-fooconfig_local'

    DOTFILE_NAME = '.fooconfig'
    BACKUP_FILE_NAME = DOTFILE_NAME[DOTFILE_NAME.rfind(os.sep) + 1 :].replace('.', '')


    @classmethod
    def setUpClass(cls):
        dfm.env = env
        dfm.ioutils.env = env
        env.set_up()
        dfm._set_args()


    def setUp(self):
        env.set_up()
        dfm._set_args()
        self.create_input_files()


    def tearDown(self):
        env.tear_down()


    def create_dotfile(self):
        ioutils._create_file(join(env.OUTPUT_DIR, self.DOTFILE_NAME), "some_bash_token=some_value")


    def clean_up_backups(self):
        shutil.rmtree(env.BACKUPS_DIR)
        os.mkdir(env.BACKUPS_DIR)


    def create_input_files(self):
        ioutils._create_file(join(env.INPUT_DIR, self.FIRST_INPUT_FILE), 'some_config_token=some_config_value')
        ioutils._create_file(join(env.INPUT_DIR, self.SECOND_INPUT_FILE), 'some_config_local_token=some_local_value')


    def test_dotfiles_reverted_when_arg_r_and_choice_y(self):
        self.create_dotfile()
        ioutils._create_file(join(env.BACKUPS_DIR, self.BACKUP_FILE_NAME + '_2016-07-07_14-40-00.bak'), "some_bash_token=some_value")
        ioutils._create_file(join(env.BACKUPS_DIR, self.BACKUP_FILE_NAME + '_2016-07-07_14-43-00.bak'), "some_bash_token=some_newer_value")

        with mock.patch('builtins.input', return_value='y'):
            dfm._revert_dotfiles([self.DOTFILE_NAME])

        with open(join(env.OUTPUT_DIR, self.DOTFILE_NAME)) as bashrc:
            contents = bashrc.read()
            self.assertTrue("some_newer_value" in contents)

        self.clean_up_backups()


    def test_dotfiles_not_reverted_when_arg_r_and_choice_n(self):
        self.create_dotfile()
        ioutils._create_file(join(env.BACKUPS_DIR, self.BACKUP_FILE_NAME + '_2016-07-07_14-40-00.bak'), "some_bash_token=some_value")
        ioutils._create_file(join(env.BACKUPS_DIR, self.BACKUP_FILE_NAME + '_2016-07-07_14-43-00.bak'), "some_bash_token=some_newer_value")

        with mock.patch('builtins.input', return_value='n'):
            dfm._revert_dotfiles([self.DOTFILE_NAME])

        with open(join(env.OUTPUT_DIR, self.DOTFILE_NAME)) as bashrc:
            self.assertTrue("some_newer_value" not in bashrc.read())

        self.clean_up_backups()


if __name__ == '__main__':
    unittest.main(module=__name__, buffer=True, exit=False)
