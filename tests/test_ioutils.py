"""Tests for dotfilesmanager.ioutils.ioutils module."""

import io
from pathlib import Path
from unittest import mock
from unittest.mock import ANY

import pytest

from dotfilesmanager.ioutils import ioutils


class TestIOUtils:
    """Tests for I/O utility functions."""

    def test_output_is_verbose_when_verbose_enabled(self, test_config, capsys):
        """Test that prints() outputs when verbose is enabled."""
        test_config.args.verbose = True

        ioutils.prints(test_config, "Compiling dotfiles!")

        captured = capsys.readouterr()
        assert "Compiling dotfiles!" in captured.out

    def test_output_is_not_verbose_when_verbose_disabled(self, test_config, capsys):
        """Test that prints() does not output when verbose is disabled."""
        test_config.args.verbose = False

        ioutils.prints(test_config, "Compiling dotfiles!")

        captured = capsys.readouterr()
        assert "Compiling dotfiles!" not in captured.out

    @mock.patch("dotfilesmanager.ioutils.ioutils._back_up")
    @mock.patch("dotfilesmanager.ioutils.ioutils.isfile", return_value=True)
    @mock.patch("builtins.open")
    def test_existing_dotfile_file_backed_up_when_not_clobber(
        self, m_open, isfile, mock_backup, test_config
    ):
        """Test that existing files are backed up when clobber is False."""
        test_config.args.clobber = False

        with io.StringIO() as buf:
            ioutils._write_output_file(test_config, str(test_config.output_dir / ".bashrc"), buf)

        mock_backup.assert_called_once()

    @mock.patch("builtins.open")
    def test_file_not_created_when_dry_run(self, m_open, test_config):
        """Test that files are not created in dry-run mode."""
        test_config.args.dry_run = True

        ioutils._create_file(test_config, "foorc", "some_token=some_value")

        m_open.assert_not_called()

    @mock.patch("dotfilesmanager.ioutils.ioutils.isfile", return_value=False)
    @mock.patch("dotfilesmanager.ioutils.ioutils.islink", return_value=False)
    @mock.patch("dotfilesmanager.ioutils.ioutils.lexists", return_value=False)
    @mock.patch("os.symlink")
    def test_symlink_created(self, mock_symlink, lexists, islink, isfile, test_config):
        """Test that symlink is created when source doesn't exist."""
        target = str(test_config.input_dir / "bashrc")
        source = str(test_config.output_dir / ".bashrc")

        ioutils.create_symlink(test_config, target, source)

        mock_symlink.assert_called_once_with(target, source)

    @mock.patch("os.symlink")
    def test_symlink_not_created_when_dry_run(self, mock_symlink, test_config):
        """Test that symlinks are not created in dry-run mode."""
        test_config.args.dry_run = True

        with mock.patch("dotfilesmanager.ioutils.ioutils.lexists", return_value=False):
            ioutils.create_symlink(
                test_config,
                str(test_config.input_dir / "bashrc"),
                str(test_config.output_dir / ".bashrc"),
            )

        mock_symlink.assert_not_called()

    def test_compile_dotfile_reads_input_files(self, test_config, temp_dirs):
        """Test that compile_dotfile reads all input files."""
        # Create test input files
        input1 = temp_dirs["input"] / "bashrc"
        input2 = temp_dirs["input"] / "bashrc_local"

        input1.write_text("export PATH=/usr/bin\n", encoding="utf-8")
        input2.write_text("export LOCAL=value\n", encoding="utf-8")

        # Compile dotfile
        ioutils.compile_dotfile(test_config, ".bashrc", ["bashrc", "bashrc_local"])

        # Verify output file was created
        output_file = temp_dirs["output"] / ".bashrc"
        assert output_file.exists()

        # Verify content from both files
        content = output_file.read_text(encoding="utf-8")
        assert "export PATH=/usr/bin" in content
        assert "export LOCAL=value" in content

    def test_back_up_creates_backup_file(self, test_config, temp_dirs):
        """Test that _back_up creates a timestamped backup."""
        # Create a file to back up
        dotfile = temp_dirs["output"] / ".bashrc"
        dotfile.write_text("original content", encoding="utf-8")

        # Back it up
        test_config.backups_dir.mkdir(parents=True, exist_ok=True)
        ioutils._back_up(test_config, str(dotfile))

        # Verify backup was created
        backups = list(test_config.backups_dir.glob("bashrc_*.bak"))
        assert len(backups) == 1
        assert backups[0].read_text(encoding="utf-8") == "original content"

    def test_back_up_creates_backups_dir_if_not_exists(self, test_config, temp_dirs):
        """Test that _back_up creates backups directory if it doesn't exist."""
        # Create a file to back up
        dotfile = temp_dirs["output"] / ".bashrc"
        dotfile.write_text("original content", encoding="utf-8")

        # Ensure backups dir doesn't exist
        if test_config.backups_dir.exists():
            import shutil

            shutil.rmtree(test_config.backups_dir)

        # Back it up
        ioutils._back_up(test_config, str(dotfile))

        # Verify backups dir was created
        assert test_config.backups_dir.exists()

    @mock.patch("builtins.input", return_value="y")
    def test_revert_dotfile_restores_latest_backup(self, mock_input, test_config, temp_dirs):
        """Test that revert_dotfile restores the latest backup."""
        # Create current dotfile
        dotfile = temp_dirs["output"] / ".bashrc"
        dotfile.write_text("current content", encoding="utf-8")

        # Create backups
        test_config.backups_dir.mkdir(parents=True, exist_ok=True)
        backup1 = test_config.backups_dir / "bashrc_2024-01-01_10-00-00.bak"
        backup2 = test_config.backups_dir / "bashrc_2024-01-02_10-00-00.bak"

        backup1.write_text("old content", encoding="utf-8")
        backup2.write_text("newer content", encoding="utf-8")

        # Revert
        ioutils.revert_dotfile(test_config, ".bashrc")

        # Verify latest backup was restored
        content = dotfile.read_text(encoding="utf-8")
        assert content == "newer content"

    @mock.patch("builtins.input", return_value="n")
    def test_revert_dotfile_cancelled_when_user_chooses_no(
        self, mock_input, test_config, temp_dirs
    ):
        """Test that revert is cancelled when user chooses 'n'."""
        # Create current dotfile
        dotfile = temp_dirs["output"] / ".bashrc"
        dotfile.write_text("current content", encoding="utf-8")

        # Create backup
        test_config.backups_dir.mkdir(parents=True, exist_ok=True)
        backup = test_config.backups_dir / "bashrc_2024-01-01_10-00-00.bak"
        backup.write_text("backup content", encoding="utf-8")

        # Attempt revert
        ioutils.revert_dotfile(test_config, ".bashrc")

        # Verify file was not changed
        content = dotfile.read_text(encoding="utf-8")
        assert content == "current content"
