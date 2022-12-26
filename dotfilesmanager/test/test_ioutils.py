import io
from os.path import join, realpath, dirname
from pathlib import Path
import sys
import unittest
from unittest import mock
from unittest.mock import ANY

TEST_DIR = str(Path(dirname(realpath(__file__))).parent)
sys.path.insert(0, TEST_DIR)

from test.env import env
import dfm
from ioutils import ioutils

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


    @mock.patch('ioutils.ioutils._back_up')
    @mock.patch('ioutils.ioutils.isfile', return_value=True)
    @mock.patch('builtins.open')
    def test_existing_dotfile_file_backed_up_when_not_arg_c(self, m_open, isfile, _back_up):
        with io.StringIO() as buf:
            ioutils._write_output_file(join(env.OUTPUT_DIR, '.bashrc'), buf)

        _back_up.assert_called_once()


    @mock.patch('dfm._get_dotfiles_dict', \
        return_value={'.fooconfig' : ['99-fooconfig', '98-fooconfig_local']})
    @mock.patch('ioutils.ioutils._write_output_file')
    def test_correct_output_file_name_written(self, _write_output_file, _get_dotfiles_dict):
        dfm._process_dotfiles(dfm._get_dotfiles_dict(env.INPUT_DIR))

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


    @mock.patch('ioutils.ioutils.os.path.exists', return_value=False)
    @mock.patch('ioutils.ioutils.os.mkdir')
    @mock.patch('ioutils.ioutils.shutil.move')
    def test_file_not_backed_up_when_arg_dry_run(self, move, mkdir, path_exists):
        env.ARGS.dry_run = True

        ioutils._back_up('foorc')

        mkdir.assert_not_called()
        move.assert_not_called()


    @mock.patch('ioutils.ioutils.glob.glob', return_value=['backup_file'])
    @mock.patch('ioutils.ioutils.os.remove')
    @mock.patch('ioutils.ioutils.shutil.copy')
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


    @mock.patch('ioutils.ioutils._back_up')
    @mock.patch('os.path.isfile', return_value=True)
    @mock.patch('os.symlink')
    def test_symlink_not_created_when_arg_dry_run(self, symlink, isfile, back_up):
        stdout = sys.stdout
        out = io.StringIO()
        sys.stdout = out
        env.ARGS.dry_run = True
        env.ARGS.verbose = True

        ioutils.create_symlink('99-foorc', 'foorc')

        symlink.assert_not_called()

        sys.stdout = stdout


    @mock.patch('os.symlink')
    @mock.patch('shutil.move')
    @mock.patch('ioutils.ioutils._remove_symlink')
    @mock.patch('os.readlink', return_value='some_nonexistent_file')
    @mock.patch('ioutils.ioutils.exists', side_effect=[False, True])
    @mock.patch('ioutils.ioutils.isfile', return_value=False)
    @mock.patch('ioutils.ioutils.lexists', return_value=True)
    def test_existing_broken_symlink_is_removed(self, lexists, isfile, exists, readlink, remove_symlink, move, symlink):
        link_target = join(env.INPUT_DIR, 'vimrc')
        link_source = join(env.OUTPUT_DIR, '.vimrc')

        ioutils.create_symlink(link_target, link_source)

        remove_symlink.assert_called_once()
        symlink.assert_called_with(link_target, link_source)


    @mock.patch('ioutils.ioutils.os.symlink')
    @mock.patch('ioutils.ioutils._remove_symlink')
    @mock.patch('ioutils.ioutils.os.readlink', return_value='vimrc')
    @mock.patch('ioutils.ioutils.exists', return_value=True)
    @mock.patch('ioutils.ioutils.isfile', return_value=False)
    @mock.patch('ioutils.ioutils.lexists', return_value=True)
    def test_dont_try_to_recreate_existing_valid_symlinked_file(self, lexists, isfile, exists, readlink, remove_symlink, symlink):
        link_target = 'vimrc'
        link_source = join(env.OUTPUT_DIR, '.vimrc')

        ioutils.create_symlink(link_target, link_source)

        remove_symlink.assert_not_called()
        symlink.assert_not_called()


    @mock.patch('ioutils.ioutils.os.symlink')
    @mock.patch('ioutils.ioutils._remove_symlink')
    @mock.patch('ioutils.ioutils.os.readlink', return_value='doom.d/')
    @mock.patch('ioutils.ioutils.exists', return_value=True)
    @mock.patch('ioutils.ioutils.isfile', return_value=False)
    @mock.patch('ioutils.ioutils.lexists', return_value=True)
    def test_dont_try_to_recreate_existing_valid_symlinked_dir(self, lexists, isfile, exists, readlink, remove_symlink, symlink):
        link_target = 'doom.d'
        link_source = join(env.OUTPUT_DIR, '.doom.d')

        ioutils.create_symlink(link_target, link_source)

        remove_symlink.assert_not_called()
        symlink.assert_not_called()


    @mock.patch('ioutils.ioutils.os.symlink')
    @mock.patch('shutil.move')
    @mock.patch('ioutils.ioutils._remove_symlink')
    @mock.patch('ioutils.ioutils.exists', return_value=True)
    def test_create_symlink_when_no_existing_symlink_source(self, exists, remove_symlink, move, symlink):
        link_target = 'vimrc'
        link_source = join(env.OUTPUT_DIR, '.vimrc')

        ioutils.create_symlink(link_target, link_source)

        remove_symlink.assert_not_called()
        symlink.assert_called_once()


    @mock.patch('ioutils.ioutils.os.path.exists', return_value=True)
    @mock.patch('ioutils.ioutils.os.mkdir')
    @mock.patch('ioutils.ioutils.shutil.move')
    def test_back_up_creates_backup(self, move, mkdir, exists):
        dotfile = '.vimrc'

        ioutils._back_up(dotfile)

        move.assert_called_once_with(dotfile, ANY)


if __name__ == '__main__':
    unittest.main(module=__name__, buffer=True, exit=False)
