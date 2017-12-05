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
        env.set_up()
        dfm._set_args()


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
    def test_existing_dotfile_file_backed_up_when_not_arg_c(self, mopen, isfile, _back_up_file):
        with io.StringIO() as buf:
            ioutils._write_output_file(join(env.OUTPUT_DIR, '.bashrc'), buf)

        _back_up_file.assert_called_once()


    @mock.patch('dotfilesmanager.dfm._get_dotfiles_dict',
        return_value={'.fooconfig' : ['99-fooconfig', '98-fooconfig_local']})
    @mock.patch('dotfilesmanager.ioutils._write_output_file')
    def test_correct_output_file_name_written(self, _write_output_file, _get_dotfiles_dict):
        dfm._compile_dotfiles(dfm._get_dotfiles_dict(env.INPUT_DIR))

        _write_output_file.assert_called_with(join(env.OUTPUT_DIR, '.fooconfig'), ANY)


if __name__ == '__main__':
    unittest.main(module=__name__, buffer=True, exit=False)
