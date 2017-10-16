#!/usr/bin/env python3.6

import io
import os
import sys
import unittest
from unittest import mock
from unittest.mock import call

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from dotfilesmanager import dfm, ioutils
from dotfilesmanager.test import env

class TestDotfilesManager(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        dfm.env = env
        dfm.ioutils.env = env


    def setUp(self):
        env.set_up()
        dfm._set_args()


    def tearDown(self):
        env.ARGS = None


    @mock.patch('dotfilesmanager.dfm._set_args')
    @mock.patch('dotfilesmanager.dfm._get_dotfiles_dict',
        return_value={'.fooconfig' : ['fooconfig', 'fooconfig_local'], '.barconfig' : ['barconfig']})
    @mock.patch('dotfilesmanager.dfm.ioutils', autospec=True)
    @mock.patch('os.path.isdir', return_value=True)
    def test_correct_branching_when_arg_r(self, isdir, ioutils, _get_dotfiles_dict, _set_args):
        env.ARGS = env.parser.parse_args(['some_dir', '-r'])

        dfm.main()

        dfm._get_dotfiles_dict.assert_called_with(env.INPUT_DIR)
        expected_calls = [call('.fooconfig'), call('.barconfig')]
        ioutils.revert_dotfile.assert_has_calls(expected_calls)


    @mock.patch('os.path.isdir', return_value=True)
    def test_output_dir_stored_in_env_when_arg_o(self, isdir):
        env.ARGS = env.parser.parse_args(['some_dir', '-o', 'some_dir'])

        dfm._set_env()

        self.assertTrue(env.OUTPUT_DIR == 'some_dir')


    @mock.patch('dotfilesmanager.dfm._set_args')
    @mock.patch('dotfilesmanager.dfm.ioutils.compile_dotfile')
    @mock.patch('os.path.isdir', return_value=True)
    @mock.patch('dotfilesmanager.dfm._get_dotfiles_dict', return_value={'.gitconfig' : ['99-gitconfig', '99-gitconfig.local']})
    def test_only_specified_dotfile_compiled_when_arg_f(self, _get_dotfiles_dict, isdir, compile_dotfile, _set_args):
        dotfile = '.gitconfig'
        input_files = ['99-gitconfig', '99-gitconfig.local']
        env.ARGS = env.parser.parse_args(['some_dir', '-f', dotfile])

        dfm.main()

        ioutils.compile_dotfile.assert_called_once()
        ioutils.compile_dotfile.assert_called_with(dotfile, input_files)


    @mock.patch('dotfilesmanager.dfm._set_args')
    @mock.patch('os.path.isdir', return_value=True)
    @mock.patch('dotfilesmanager.dfm._get_dotfiles_dict', return_value={'.gitconfig' : ['gitconfig', 'gitconfig_local']})
    def test_print_error_exit_1_when_arg_f_and_invalid_dotfile_name(self, _get_dotfiles_dict, isdir, _set_args):
        stderr = sys.stderr
        err = io.StringIO()
        sys.stderr = err
        dfm.env.ARGS = env.parser.parse_args(['some_dir', '-f', 'foobar'])

        with self.assertRaises(SystemExit) as se:
            dfm.main()

        self.assertEqual(se.exception.code, 1)
        self.assertTrue("No input files found" in err.getvalue())

        sys.stderr = stderr


    @mock.patch('dotfilesmanager.dfm._set_args')
    @mock.patch('dotfilesmanager.dfm.ioutils')
    @mock.patch('dotfilesmanager.dfm._get_dotfiles_dict', return_value={})
    @mock.patch('os.path.isdir', return_value=True)
    def test_only_specified_file_reverted_when_args_rf(self, isdir, _get_dotfiles_dict, ioutils, _set_args):
        env.ARGS = env.parser.parse_args(['some_dir', '-r', '-f', '.bashrc'])

        dfm.main()

        ioutils.revert_dotfile.assert_called_with('.bashrc')
        ioutils.compile_dotfile.assert_not_called()


    @mock.patch('dotfilesmanager.dfm._set_args')
    @mock.patch('dotfilesmanager.dfm.ioutils')
    @mock.patch('os.path.isdir', return_value=False)
    def test_print_error_exit_1_when_invalid_input_dir(self, isdir, ioutils, _set_args):
        stderr = sys.stderr
        err = io.StringIO()
        sys.stderr = err
        input_dir = 'some_nonexistent_dir'
        env.ARGS = env.parser.parse_args(['-r', input_dir])

        with self.assertRaises(SystemExit) as se:
            dfm._set_env()

        self.assertEqual(se.exception.code, 1)
        self.assertTrue("Specified input directory {0} does not exist.".format(input_dir) in err.getvalue())

        sys.stderr = stderr


    @mock.patch('dotfilesmanager.dfm._set_args')
    @mock.patch('os.path.isdir', return_value=True)
    @mock.patch('os.path.isfile', return_value=True)
    @mock.patch('os.listdir', return_value=['foorc', 'foorc_local', 'bar.config'])
    @mock.patch('dotfilesmanager.ioutils.compile_dotfile')
    def test_dotfiles_compiled_by_input_file_name_convention(self, compile_dotfile, listdir, isfile, isdir, set_args):
        env.ARGS = env.parser.parse_args(['some_dir'])
        expected_calls = [call('.foorc', ['foorc', 'foorc_local']), call('.bar.config', ['bar.config'])]

        dfm.main()

        ioutils.compile_dotfile.assert_has_calls(expected_calls)


    @mock.patch('dotfilesmanager.ioutils.os.listdir', return_value=['99-gitconfig', '98-gitconfig_local', 'vimrc', '99-bashrc', 'bashrc_local'])
    @mock.patch('dotfilesmanager.ioutils.os.path.isfile', return_value=True)
    def test_get_dotfiles_dict(self, listdir, isfile):
        expected = set({
            '.gitconfig' : ['.gitconfig'],
            '.vimrc': ['vimrc'],
            '.bashrc': ['99-bashrc', 'bashrc_local']
            })

        self.assertEqual(set(dfm._get_dotfiles_dict(env.INPUT_DIR)), expected)


    @mock.patch('dotfilesmanager.dfm._set_args')
    @mock.patch('dotfilesmanager.dfm.os.listdir',
        return_value=['gitconfig', 'gitconfig_local', 'bashrc', 'bashrc_local'])
    @mock.patch('dotfilesmanager.dfm.ioutils.os.path.isdir', return_value=True)
    @mock.patch('dotfilesmanager.dfm.ioutils.os.path.isfile', return_value=True)
    @mock.patch('ioutils._write_input_file_contents')
    def test_when_arg_e_then_specified_files_are_excluded(self, _write_input_file_contents, isfile, isdir, listdir, _set_args):
        env.ARGS = env.parser.parse_args([
            'some_dir',
            '-e', 'gitconfig_local',
            '-e', 'bashrc_local'
        ])

        actual_dict = dfm._get_dotfiles_dict(env.INPUT_DIR)

        self.assertTrue('gitconfig_local' not in actual_dict['.gitconfig'])
        self.assertTrue('bashrc_local' not in actual_dict['.bashrc'])


    @mock.patch('os.path.isfile', return_value=True)
    def test_get_dotfile_name_from_input_filename(self, isfile):
        input_files = ['gitconfig_local', '99-vimrc', '99-tmux.conf_local', '98-tmux.conf', 'bashrc_mac-gnu']
        dotfile_names = []

        for input_file in input_files:
            dotfile_names.append(dfm._get_dotfile_name(input_file))

        self.assertEqual(set(dotfile_names), set(['.gitconfig', '.tmux.conf', '.vimrc', '.bashrc']))


if __name__ == '__main__':
    unittest.main(module=__name__, buffer=True, exit=False)