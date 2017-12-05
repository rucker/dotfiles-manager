#!/usr/bin/env python3.6

import io
import os
from os.path import join
import sys
import unittest
from unittest import mock
from unittest.mock import ANY

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from dotfilesmanager.test import env
from dotfilesmanager import dfm
from dotfilesmanager import ioutils

class TestIOUtils(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        dfm.env = env
        dfm.ioutils.env = env


    def setUp(self):
        env.set_up()
        dfm._set_args()


    def tearDown(self):
        env.tear_down()


    def test_output_is_verbose_when_arg_v(self):
        stdout = sys.stdout
        out = io.StringIO()
        sys.stdout = out
        env.ARGS = env.parser.parse_args(['some_dir', '-v'])

        ioutils.sprint("Compiling dotfiles!")

        self.assertTrue("Compiling dotfiles!" in out.getvalue())

        sys.stdout = stdout

    def test_output_is_not_verbose_when_not_arg_v(self):
        stdout = sys.stdout
        out = io.StringIO()
        sys.stdout = out

        ioutils.sprint("Compiling dotfiles!")

        self.assertFalse("Compiling dotfiles!" in out.getvalue())

        sys.stdout = stdout


    @mock.patch('dotfilesmanager.ioutils._back_up_file')
    @mock.patch('dotfilesmanager.ioutils.isfile', return_value=True)
    @mock.patch('builtins.open')
    def test_existing_dotfile_file_backed_up_when_not_arg_c(self, m_open, isfile, _back_up_file):
        with io.StringIO() as buf:
            ioutils._write_output_file(join(env.OUTPUT_DIR, '.bashrc'), buf)

        _back_up_file.assert_called_once()


    @mock.patch('dotfilesmanager.dfm._get_dotfiles_dict', \
        return_value={'.fooconfig' : ['99-fooconfig', '98-fooconfig_local']})
    @mock.patch('dotfilesmanager.ioutils._write_output_file')
    def test_correct_output_file_name_written(self, _write_output_file, _get_dotfiles_dict):
        dfm._compile_dotfiles(dfm._get_dotfiles_dict(env.INPUT_DIR))

        _write_output_file.assert_called_with(join(env.OUTPUT_DIR, '.fooconfig'), ANY)


    @mock.patch('builtins.open')
    def test_file_not_created_when_arg_dry_run(self, m_open):
        stdout = sys.stdout
        out = io.StringIO()
        sys.stdout = out
        env.ARGS.dry_run = True
        env.ARGS.verbose = True

        ioutils._create_file('foorc', 'some_token=some_value')

        m_open.assert_not_called()

        sys.stdout = stdout


    @mock.patch('ioutils.os.path.exists', return_value=False)
    @mock.patch('ioutils.os.mkdir')
    @mock.patch('ioutils.shutil.move')
    def test_file_not_backed_up_when_arg_dry_run(self, move, mkdir, path_exists):
        env.ARGS.dry_run = True

        ioutils._back_up_file('foorc')

        mkdir.assert_not_called()
        move.assert_not_called()


    @mock.patch('ioutils.glob.glob', return_value=['backup_file'])
    @mock.patch('ioutils.os.remove')
    @mock.patch('ioutils.shutil.copy')
    def test_file_not_reverted_when_arg_dry_run(self, copy, remove, glob):
        stdout = sys.stdout
        out = io.StringIO()
        sys.stdout = out

        env.ARGS.dry_run = True
        env.ARGS.verbose = True

        with mock.patch('builtins.input', return_value='y'):
            ioutils.revert_dotfile('foorc')

        copy.assert_not_called()
        remove.assert_not_called()
        self.assertTrue("foorc and replacing" in out.getvalue())

        sys.stdout = stdout


    @mock.patch('builtins.open')
    def test_output_file_not_written_when_arg_dry_run(self, m_open):
        stdout = sys.stdout
        out = io.StringIO()
        sys.stdout = out
        env.ARGS.dry_run = True
        env.ARGS.verbose = True

        ioutils._write_output_file('foorc', io.StringIO())

        m_open.assert_not_called()

        sys.stdout = stdout


if __name__ == '__main__':
    unittest.main(module=__name__, buffer=True, exit=False)
