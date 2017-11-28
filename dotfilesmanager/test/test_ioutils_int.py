#!/usr/bin/env python3.6

import io
import os
from os.path import join
import shutil
import sys
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from dotfilesmanager.test import env
from dotfilesmanager import dfm
from dotfilesmanager import ioutils


class TestIOUtilsInt(unittest.TestCase):

    FIRST_INPUT_FILE = '99-fooconfig'
    SECOND_INPUT_FILE = '98-fooconfig_local'

    DOTFILE_NAME = '.fooconfig'
    BACKUP_FILE_NAME = DOTFILE_NAME[DOTFILE_NAME.rfind('/') + 1 :].replace('.', '')


    @classmethod
    def setUpClass(cls):
        dfm.env = env
        dfm.ioutils.env = env
        env.set_up()
        cls.create_input_files(cls)


    def setUp(self):
        env.set_up()
        dfm._set_args()


    @classmethod
    def tearDownClass(cls):
        env.tear_down()


    def create_dotfile(self):
        ioutils._create_file(join(env.OUTPUT_DIR, self.DOTFILE_NAME), "some_bash_token=some_value")


    def clean_up_backups(self):
        shutil.rmtree(env.BACKUPS_DIR)
        os.mkdir(env.BACKUPS_DIR)


    def create_input_files(self):
        ioutils._create_file(join(env.INPUT_DIR, self.FIRST_INPUT_FILE), 'some_config_token=some_config_value')
        ioutils._create_file(join(env.INPUT_DIR, self.SECOND_INPUT_FILE), 'some_config_local_token=some_local_value')


    def test_existing_dotfile_backed_up_when_not_arg_c(self):
        self.create_dotfile()
        with io.StringIO() as buf:
            buf.write(str("some_bash_token=some_newer_value"))
            ioutils._write_output_file(join(env.OUTPUT_DIR, self.DOTFILE_NAME), buf)
        backup_files = os.listdir(env.BACKUPS_DIR)
        self.assertTrue(len(backup_files) is 1)

        with open(join(env.BACKUPS_DIR, backup_files[0])) as bak_file:
            self.assertTrue("some_value" in bak_file.read())

        self.clean_up_backups()


    def test_output_file_contains_all_input_files_in_correct_order(self):
        line_1 = 'first-token\n'
        line_2 = 'second-token\n'
        line_3 = 'third-token\n'
        ioutils._create_file(join(env.INPUT_DIR, self.FIRST_INPUT_FILE), line_1)
        ioutils._create_file(join(env.INPUT_DIR, self.SECOND_INPUT_FILE), line_2)
        ioutils._create_file(join(env.INPUT_DIR, 'fooconfig'), line_3)

        dfm._compile_dotfiles(dfm._get_dotfiles_dict(env.INPUT_DIR))

        with open(join(env.OUTPUT_DIR, self.DOTFILE_NAME)) as fooconfig:
            file_contents = fooconfig.readlines()
            self.assertEqual(file_contents[0], line_1)

        self.clean_up_backups()
        os.remove(join(env.INPUT_DIR, 'fooconfig'))


    def test_when_arg_e_then_specified_file_is_excluded(self):
        env.ARGS = env.parser.parse_args(['some_dir', '-e', self.SECOND_INPUT_FILE])
        ioutils._create_file(join(env.OUTPUT_DIR, self.FIRST_INPUT_FILE), "some_token=some_value")
        ioutils._create_file(join(env.OUTPUT_DIR, self.SECOND_INPUT_FILE), "some_local_token=some_value")

        dfm._compile_dotfiles(dfm._get_dotfiles_dict(env.INPUT_DIR))

        with open(join(env.OUTPUT_DIR, self.DOTFILE_NAME)) as output_file:
            with open(join(env.INPUT_DIR, self.FIRST_INPUT_FILE)) as input_file:
                with open(join(env.INPUT_DIR, self.SECOND_INPUT_FILE)) as \
                local_input_file:
                    contents = output_file.read()
                    self.assertTrue(input_file.read() in contents)
                    self.assertTrue(local_input_file.read() not in contents)
        env.ARGS = None


if __name__ == '__main__':
    unittest.main(module=__name__, buffer=True, exit=False)
