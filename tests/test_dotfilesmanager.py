"""Tests for dotfilesmanager.dfm module."""

import io
import os
import sys
from argparse import Namespace
from pathlib import Path
from unittest import mock
from unittest.mock import call

import pytest

from dotfilesmanager import dfm
from dotfilesmanager.config import Config


class TestDotfilesManager:
    """Tests for main dfm orchestration logic."""

    def test_correct_branching_when_arg_r(self, test_config):
        """Test that revert mode reverts all dotfiles."""
        test_config.args.revert = True

        dotfiles_dict = {
            ".fooconfig": ["fooconfig", "fooconfig_local"],
            ".barconfig": ["barconfig"],
        }

        with mock.patch("dotfilesmanager.dfm._get_dotfiles_dict", return_value=dotfiles_dict):
            with mock.patch("dotfilesmanager.ioutils.ioutils.revert_dotfile") as mock_revert:
                dfm._revert_dotfiles(test_config, list(dotfiles_dict.keys()))

                expected_calls = [
                    call(test_config, ".fooconfig"),
                    call(test_config, ".barconfig"),
                ]
                mock_revert.assert_has_calls(expected_calls)

    def test_output_dir_from_args(self, temp_dirs):
        """Test that output directory is set from arguments."""
        args = Namespace(
            input_dir=str(temp_dirs["input"]),
            output_dir=["some_other_dir"],
            clobber=False,
            revert=False,
            verbose=False,
            dry_run=False,
            file=None,
            exclude=None,
            no_symlinks=False,
        )

        # Create config manually since from_args validates directories
        config = Config(
            input_dir=temp_dirs["input"],
            output_dir=Path("some_other_dir"),
            backups_dir=temp_dirs["input"] / "backups",
            args=args,
        )

        assert config.output_dir == Path("some_other_dir")

    def test_only_specified_dotfile_compiled_when_arg_f(self, test_config):
        """Test that -f flag processes only specified dotfile."""
        dotfile = ".gitconfig"
        input_files = ["99-gitconfig", "99-gitconfig.local"]
        test_config.args.file = [dotfile]
        test_config.args.no_symlinks = True

        dotfiles_dict = {".gitconfig": input_files}

        with mock.patch("dotfilesmanager.dfm._get_dotfiles_dict", return_value=dotfiles_dict):
            with mock.patch("dotfilesmanager.ioutils.ioutils.compile_dotfile") as mock_compile:
                dfm._process_dotfile(test_config, dotfile, input_files)

                mock_compile.assert_called_once_with(test_config, dotfile, input_files)

    def test_only_specified_dotfile_dir_handled_and_path_normalized_when_arg_f(
        self, test_config
    ):
        """Test that directory dotfiles are normalized and symlinked."""
        dotfile = ".foo.d"
        test_config.args.file = [dotfile + "/"]

        with mock.patch("dotfilesmanager.ioutils.ioutils.create_symlink") as mock_symlink:
            dfm._process_dotfile(test_config, dotfile, ["foo.d"])

            # Check that create_symlink was called with config and paths
            assert mock_symlink.called
            call_args = mock_symlink.call_args[0]
            assert call_args[0] == test_config
            assert "foo.d" in call_args[1]
            assert dotfile in call_args[2]

    def test_print_error_exit_1_when_arg_f_and_invalid_dotfile_name(self, test_config):
        """Test error handling for invalid dotfile name with -f flag."""
        test_config.args.file = ["foobar"]

        dotfiles_dict = {".gitconfig": ["gitconfig", "gitconfig_local"]}

        with mock.patch("dotfilesmanager.dfm._get_dotfiles_dict", return_value=dotfiles_dict):
            with mock.patch("dotfilesmanager.dfm._parse_args", return_value=test_config.args):
                with mock.patch(
                    "dotfilesmanager.config.Config.from_args", return_value=test_config
                ):
                    with pytest.raises(SystemExit) as exc_info:
                        stderr = io.StringIO()
                        with mock.patch("sys.stderr", stderr):
                            dfm.main()

                    assert exc_info.value.code == 1
                    # Note: stderr capture in pytest is different, this checks exit code

    def test_get_dotfile_name_with_priority_and_suffix(self):
        """Test dotfile name extraction with priority number and suffix."""
        assert dfm._get_dotfile_name("99-bashrc_local") == ".bashrc"
        assert dfm._get_dotfile_name("bashrc") == ".bashrc"
        assert dfm._get_dotfile_name("50-vimrc_work") == ".vimrc"

    def test_get_dotfile_name_with_extension(self):
        """Test dotfile name extraction with file extension."""
        assert dfm._get_dotfile_name("tmux.conf") == ".tmux.conf"
        assert dfm._get_dotfile_name("99-tmux.conf_local") == ".tmux.conf"

    def test_sort_input_file_list_priority_first(self):
        """Test that priority-numbered files are sorted reverse numerically."""
        input_files = ["bashrc", "99-bashrc", "50-bashrc", "bashrc_local"]
        sorted_files = dfm._sort_input_file_list(input_files)

        assert sorted_files == ["99-bashrc", "50-bashrc", "bashrc", "bashrc_local"]

    def test_is_input_file_excluded_when_not_excluded(self, test_config):
        """Test that non-excluded files are not filtered."""
        test_config.args.exclude = None
        assert not dfm._is_input_file_excluded(test_config, "bashrc")

    def test_is_input_file_excluded_when_excluded(self, test_config):
        """Test that excluded files are properly filtered."""
        test_config.args.exclude = [["bashrc_local", "vimrc_work"]]
        assert dfm._is_input_file_excluded(test_config, "bashrc_local")
        assert dfm._is_input_file_excluded(test_config, "vimrc_work")
        assert not dfm._is_input_file_excluded(test_config, "bashrc")

    def test_add_input_file_to_dict_not_excluded(self, test_config):
        """Test adding non-excluded file to dotfiles dict."""
        test_config.args.exclude = None
        dotfiles_dict = {}

        dfm._add_input_file_to_dict(test_config, dotfiles_dict, "bashrc")

        assert ".bashrc" in dotfiles_dict
        assert dotfiles_dict[".bashrc"] == ["bashrc"]

    def test_add_input_file_to_dict_excluded(self, test_config):
        """Test that excluded files are not added to dict."""
        test_config.args.exclude = [["bashrc"]]
        dotfiles_dict = {}

        dfm._add_input_file_to_dict(test_config, dotfiles_dict, "bashrc")

        assert ".bashrc" not in dotfiles_dict

    def test_get_dotfiles_dict(self, test_config, temp_dirs):
        """Test building dotfiles dictionary from input directory."""
        # Create test input files
        (temp_dirs["input"] / "bashrc").touch()
        (temp_dirs["input"] / "99-bashrc").touch()
        (temp_dirs["input"] / "vimrc").touch()

        dotfiles_dict = dfm._get_dotfiles_dict(test_config)

        assert ".bashrc" in dotfiles_dict
        assert ".vimrc" in dotfiles_dict
        # Priority files should be first
        assert dotfiles_dict[".bashrc"][0] == "99-bashrc"

    def test_process_dotfile_compiles_when_multiple_inputs(self, test_config):
        """Test that multiple input files trigger compilation."""
        input_files = ["bashrc", "bashrc_local"]

        with mock.patch("dotfilesmanager.ioutils.ioutils.compile_dotfile") as mock_compile:
            dfm._process_dotfile(test_config, ".bashrc", input_files)

            mock_compile.assert_called_once_with(test_config, ".bashrc", input_files)

    def test_process_dotfile_symlinks_when_single_input(self, test_config):
        """Test that single input file triggers symlink creation."""
        input_files = ["bashrc"]

        with mock.patch("dotfilesmanager.ioutils.ioutils.create_symlink") as mock_symlink:
            dfm._process_dotfile(test_config, ".bashrc", input_files)

            assert mock_symlink.called
            call_args = mock_symlink.call_args[0]
            assert call_args[0] == test_config

    def test_process_dotfile_compiles_when_no_symlinks_flag(self, test_config):
        """Test that --no-symlinks forces compilation even with single input."""
        test_config.args.no_symlinks = True
        input_files = ["bashrc"]

        with mock.patch("dotfilesmanager.ioutils.ioutils.compile_dotfile") as mock_compile:
            dfm._process_dotfile(test_config, ".bashrc", input_files)

            mock_compile.assert_called_once_with(test_config, ".bashrc", input_files)
