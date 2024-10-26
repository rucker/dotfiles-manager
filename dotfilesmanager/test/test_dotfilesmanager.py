import io
from os.path import join, realpath, dirname, normpath
from pathlib import Path
import sys
import unittest
from unittest import mock
from unittest.mock import call

TEST_DIR = str(Path(dirname(realpath(__file__))).parent)
sys.path.insert(0, TEST_DIR)

from test.env import env
import dfm


class TestDotfilesManager(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        dfm.env = env
        dfm.ioutils.env = env


    def setUp(self):
        env.set_up()
        dfm._set_args()


    def tearDown(self):
        env.tear_down()


    @mock.patch('dfm._set_args')
    @mock.patch('dfm._get_dotfiles_dict', \
        return_value={'.fooconfig' : ['fooconfig', 'fooconfig_local'], '.barconfig' : ['barconfig']})
    @mock.patch('dfm.ioutils', autospec=True)
    @mock.patch('os.path.isdir', return_value=True)
    def test_correct_branching_when_arg_r(self, isdir, ioutils, _get_dotfiles_dict, _set_args):
        env.ARGS = env.parser.parse_args(['some_dir', '-r'])

        dfm.main()

        dfm._get_dotfiles_dict.assert_called_with(env.INPUT_DIR)
        expected_calls = [call('.fooconfig'), call('.barconfig')]
        ioutils.revert_dotfile.assert_has_calls(expected_calls)


    @mock.patch('os.path.isdir', return_value=True)
    def test_output_dir_stored_in_env_when_arg_o(self, isdir):
        env.ARGS = env.parser.parse_args(['some_dir', '-o', 'some_other_dir'])

        dfm._set_env()

        self.assertTrue(env.OUTPUT_DIR == 'some_other_dir')


    @mock.patch('dfm._set_args')
    @mock.patch('dfm.ioutils.compile_dotfile')
    @mock.patch('os.path.isdir', return_value=True)
    @mock.patch('dfm._get_dotfiles_dict', return_value={'.gitconfig' : ['99-gitconfig', '99-gitconfig.local']})
    def test_only_specified_dotfile_compiled_when_arg_f(self, _get_dotfiles_dict, isdir, compile_dotfile, _set_args):
        dotfile = '.gitconfig'
        input_files = ['99-gitconfig', '99-gitconfig.local']
        env.ARGS = env.parser.parse_args(['some_dir', '-f', dotfile])

        dfm.main()

        compile_dotfile.assert_called_once_with(dotfile, input_files)


    @mock.patch('dfm._set_args')
    @mock.patch('dfm.ioutils.create_symlink')
    @mock.patch('os.path.isdir', return_value=True)
    @mock.patch('dfm._get_dotfiles_dict', return_value={'.foo.d' : ['foo.d']})
    def test_only_specified_dotfile_dir_handled_and_path_normalized_when_arg_f(self, _get_dotfiles_dict, isdir, create_symlink, _set_args):
        dotfile = '.foo.d/'
        env.ARGS = env.parser.parse_args(['some_dir', '-f', dotfile])

        dfm.main()

        create_symlink.assert_called_once_with(join(env.INPUT_DIR, 'foo.d'), \
                normpath(join(env.OUTPUT_DIR, dotfile)))


    @mock.patch('dfm._set_args')
    @mock.patch('os.path.isdir', return_value=True)
    @mock.patch('dfm._get_dotfiles_dict', return_value={'.gitconfig' : ['gitconfig', 'gitconfig_local']})
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


    @mock.patch('dfm._set_args')
    @mock.patch('dfm.ioutils')
    @mock.patch('dfm._get_dotfiles_dict', return_value={})
    @mock.patch('os.path.isdir', return_value=True)
    def test_only_specified_file_reverted_when_args_rf(self, isdir, _get_dotfiles_dict, ioutils, _set_args):
        env.ARGS = env.parser.parse_args(['some_dir', '-r', '-f', '.bashrc'])

        dfm.main()

        ioutils.revert_dotfile.assert_called_with('.bashrc')
        ioutils.compile_dotfile.assert_not_called()


    @mock.patch('dfm._set_args')
    @mock.patch('dfm.ioutils')
    @mock.patch('dfm._get_dotfiles_dict', return_value={})
    @mock.patch('os.path.isdir', return_value=True)
    def test_only_specified_dir_reverted_when_args_rf(self, isdir, _get_dotfiles_dict, ioutils, _set_args):
        env.ARGS = env.parser.parse_args(['some_dir', '-r', '-f', '.foo.d/'])

        dfm.main()

        ioutils.revert_dotfile.assert_called_with('.foo.d')
        ioutils.compile_dotfile.assert_not_called()


    @mock.patch('dfm._set_args')
    @mock.patch('dfm.ioutils')
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
        self.assertTrue(f"Specified input directory {input_dir} does not exist." in err.getvalue())

        sys.stderr = stderr


    @mock.patch('dfm._set_args')
    @mock.patch('os.path.isdir', return_value=True)
    @mock.patch('os.path.isfile', return_value=True)
    @mock.patch('os.listdir', return_value=['foorc', 'foorc_local', '99-bar.config', 'bar.config'])
    @mock.patch('ioutils.ioutils.compile_dotfile')
    def test_dotfiles_compiled_by_input_file_name_convention(self, compile_dotfile, listdir, isfile, isdir, set_args):
        env.ARGS = env.parser.parse_args(['some_dir'])
        expected_calls = [call('.foorc', ['foorc', 'foorc_local']), \
                call('.bar.config', ['99-bar.config', 'bar.config'])]

        dfm.main()

        compile_dotfile.assert_has_calls(expected_calls)


    @mock.patch('ioutils.ioutils.os.listdir', return_value=['99-gitconfig', '98-gitconfig_local', 'vimrc', '99-bashrc', 'bashrc_local'])
    @mock.patch('ioutils.ioutils.os.path.isfile', return_value=True)
    def test_get_dotfiles_dict(self, listdir, isfile):
        expected = set({
            '.gitconfig' : ['.gitconfig'],
            '.vimrc': ['vimrc'],
            '.bashrc': ['99-bashrc', 'bashrc_local']
            })

        self.assertEqual(set(dfm._get_dotfiles_dict(env.INPUT_DIR)), expected)


    @mock.patch('dfm._set_args')
    @mock.patch('dfm.os.listdir', \
        return_value=['gitconfig', 'gitconfig_local', 'bashrc', 'bashrc_local'])
    @mock.patch('dfm.ioutils.os.path.isdir', return_value=True)
    @mock.patch('dfm.ioutils.os.path.isfile', return_value=True)
    @mock.patch('ioutils.ioutils._write_input_file_contents')
    def test_when_arg_e_then_specified_files_are_not_mapped_for_processing(self, _write_input_file_contents, isfile, isdir, listdir, _set_args):
        env.ARGS = env.parser.parse_args([
            'some_dir',
            '-e', 'gitconfig_local',
            '-e', 'bashrc_local'
        ])

        actual_dict = dfm._get_dotfiles_dict(env.INPUT_DIR)

        self.assertTrue('gitconfig_local' not in actual_dict['.gitconfig'])
        self.assertTrue('bashrc_local' not in actual_dict['.bashrc'])


    @mock.patch('dfm._set_args')
    @mock.patch('dfm.os.listdir', \
        return_value=['bashrc', 'bashrc_local'])
    @mock.patch('dfm.ioutils.os.path.isdir', return_value=True)
    @mock.patch('dfm.ioutils.os.path.isfile', return_value=True)
    @mock.patch('dfm._process_dotfile')
    @mock.patch('ioutils.ioutils._write_input_file_contents')
    def test_when_arg_e_and_arg_f_then_specified_file_is_not_processed(self, _write_input_file_contents, _process_dotfile, isfile, isdir, listdir, _set_args):
        env.ARGS = env.parser.parse_args([
            'some_dir',
            '-e', 'bashrc',
            '-f', 'bashrc'
        ])

        dfm.main()

        self.assertEqual(_process_dotfile.call_count, 0)


    @mock.patch('os.path.isfile', return_value=True)
    def test_get_dotfile_name_from_input_filename(self, isfile):
        input_files = ['gitconfig_local', '99-vimrc', '99-tmux.conf_local', '98-tmux.conf', 'bashrc_mac-gnu']
        dotfile_names = []

        for input_file in input_files:
            dotfile_names.append(dfm._get_dotfile_name(input_file))

        self.assertEqual(set(dotfile_names), set(['.gitconfig', '.tmux.conf', '.vimrc', '.bashrc']))


    @mock.patch('dfm.ioutils.os.path.isdir', return_value=True)
    def test_error_when_input_dir_same_as_output_dir(self, isdir):
        stderr = sys.stderr
        err = io.StringIO()
        sys.stderr = err
        user_home_dir = 'my_home_dir'
        env.OUTPUT_DIR = user_home_dir
        env.ARGS = env.parser.parse_args([user_home_dir])

        with self.assertRaises(SystemExit) as sys_exit:
            dfm._set_env()
        self.assertEqual(sys_exit.exception.code, 1)
        self.assertTrue(f"INPUT_DIR {user_home_dir} cannot be the same as OUTPUT_DIR {user_home_dir}")

        sys.stderr = stderr


    @mock.patch('dfm.ioutils.os.path.isdir', return_value=True)
    def test_arg_dry_run_implies_arg_verbose(self, isdir):
        stdout = sys.stdout
        out = io.StringIO()
        sys.stdout = out
        dfm._set_args()
        env.ARGS = env.parser.parse_args(['some_dir', '--dry-run'])

        dfm._set_env()

        self.assertTrue(env.ARGS.dry_run)
        self.assertTrue(env.ARGS.verbose)

        sys.stdout = stdout


    @mock.patch('os.path.isdir', return_value=True)
    @mock.patch('dfm._set_args')
    @mock.patch('dfm.ioutils.create_symlink')
    @mock.patch('dfm._get_dotfiles_dict', return_value={'.fooconfig' : ['fooconfig']})
    def test_symlink_created_when_single_input_file(self, get_dotfiles_dict, create_symlink, set_args, isdir):
        env.ARGS = env.parser.parse_args(['some_dir'])

        dfm.main()

        create_symlink.assert_called_once_with(join(env.INPUT_DIR, 'fooconfig'), \
                join(env.OUTPUT_DIR, '.fooconfig'))


    @mock.patch('builtins.open')
    @mock.patch('ioutils.ioutils._remove_symlink')
    @mock.patch('ioutils.ioutils.islink', return_value=True)
    @mock.patch('dfm.ioutils._back_up')
    @mock.patch('os.path.isdir', return_value=True)
    @mock.patch('dfm._set_args')
    @mock.patch('dfm.ioutils.create_symlink')
    @mock.patch('dfm._get_dotfiles_dict', return_value={'.fooconfig' : ['99-fooconfig', 'fooconfig']})
    def test_existing_symlink_removed_when_multiple_input_files(self, get_dotfiles_dict, create_symlink, set_args, isdir, back_up, islink, remove_symlink, m_open):
        env.ARGS = env.parser.parse_args(['some_dir'])

        dfm.main()

        back_up.assert_not_called()
        remove_symlink.assert_called_once()


    @mock.patch('os.path.isdir', return_value=True)
    @mock.patch('ioutils.ioutils.lexists', return_value=True)
    @mock.patch('dfm._set_args')
    @mock.patch('ioutils.ioutils.os.readlink', return_value='vimrc')
    @mock.patch('dfm.ioutils._back_up')
    @mock.patch('dfm.ioutils.islink', return_value=False)
    @mock.patch('dfm.ioutils.exists', return_value=True)
    @mock.patch('dfm.ioutils.os.symlink')
    @mock.patch('dfm._get_dotfiles_dict', return_value={'.fooconfig' : ['fooconfig']})
    def test_existing_dotfile_replaced_with_symlink_when_single_input_file(self, get_dotfiles_dict, symlink, isfile, islink, back_up, readlink, set_args, lexists, isdir):
        env.ARGS = env.parser.parse_args(['some_dir'])

        dfm.main()

        input_file = join(env.INPUT_DIR, 'fooconfig')
        output_file = join(env.OUTPUT_DIR, '.fooconfig')
        back_up.assert_called_once_with(output_file)
        symlink.assert_called_once_with(input_file, output_file)


    @mock.patch('os.path.isdir', return_value=True)
    @mock.patch('dfm._set_args')
    @mock.patch('dfm.ioutils.compile_dotfile')
    @mock.patch('dfm.ioutils.create_symlink')
    @mock.patch('dfm._get_dotfiles_dict', return_value={'.fooconfig' : ['fooconfig']})
    def test_symlinks_not_created_when_arg_no_symlinks(self, get_dotfiles_dict, create_symlink, compile_dotfile, set_args, isdir):
        env.ARGS = env.parser.parse_args(['some_dir', '--no-symlinks'])

        dfm.main()

        dotfile = '.fooconfig'
        input_files = ['fooconfig']

        create_symlink.assert_not_called()
        compile_dotfile.assert_called_once_with(dotfile, input_files)

    @mock.patch('os.path.isdir', return_value=True)
    @mock.patch('os.listdir', return_value=['foo.d'])
    @mock.patch('os.path.isfile', return_value=False)
    @mock.patch('dfm._set_args')
    @mock.patch('dfm.ioutils.compile_dotfile')
    @mock.patch('dfm.ioutils.create_symlink')
    def test_symlink_to_dir_when_input_dir_contains_dir(self, create_symlink, compile_dotfile, set_args, isfile, listdir, isdir):
        env.ARGS = env.parser.parse_args(['some_dir'])

        dfm.main()

        create_symlink.assert_called_once_with(join(env.INPUT_DIR, 'foo.d'), \
                join(env.OUTPUT_DIR, '.foo.d'))


    def test_excluded_dir_name_args_are_normalized(self):
        env.ARGS = env.parser.parse_args(['some_dir', '-e', 'foo.d/'])

        is_excluded = dfm._is_input_file_excluded('foo.d')

        self.assertTrue(is_excluded)

if __name__ == '__main__':
    unittest.main(module=__name__, buffer=True, exit=False)
