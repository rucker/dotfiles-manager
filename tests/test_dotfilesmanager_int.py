"""Integration tests for dotfilesmanager.dfm module."""

import os
from pathlib import Path
from unittest import mock

import pytest

from dotfilesmanager import dfm
from dotfilesmanager.ioutils import ioutils


class TestDotfilesManagerInt:
    """Integration tests for dotfiles manager."""

    FIRST_INPUT_FILE = "99-fooconfig"
    SECOND_INPUT_FILE = "98-fooconfig_local"
    DOTFILE_NAME = ".fooconfig"
    BACKUP_FILE_NAME = "fooconfig"

    @pytest.fixture(autouse=True)
    def setup(self, test_config):
        """Set up test environment for each test."""
        self.config = test_config
        self.create_input_files()

    def create_dotfile(self):
        """Create a test dotfile in output directory."""
        dotfile_path = self.config.output_dir / self.DOTFILE_NAME
        dotfile_path.write_text("some_bash_token=some_value", encoding="utf-8")

    def clean_up_backups(self):
        """Clean up backup directory."""
        if self.config.backups_dir.exists():
            import shutil

            shutil.rmtree(self.config.backups_dir)
        self.config.backups_dir.mkdir(parents=True, exist_ok=True)

    def create_input_files(self):
        """Create test input files."""
        first_file = self.config.input_dir / self.FIRST_INPUT_FILE
        second_file = self.config.input_dir / self.SECOND_INPUT_FILE

        first_file.write_text("some_config_token=some_config_value", encoding="utf-8")
        second_file.write_text("some_config_local_token=some_local_value", encoding="utf-8")

    def test_dotfiles_reverted_when_arg_r_and_choice_y(self):
        """Test that dotfiles are reverted when user chooses 'y'."""
        # Create a dotfile and backups
        self.create_dotfile()
        self.config.backups_dir.mkdir(parents=True, exist_ok=True)

        backup1 = self.config.backups_dir / f"{self.BACKUP_FILE_NAME}_2016-07-07_14-40-00.bak"
        backup2 = self.config.backups_dir / f"{self.BACKUP_FILE_NAME}_2016-07-07_14-43-00.bak"

        backup1.write_text("some_bash_token=some_value", encoding="utf-8")
        backup2.write_text("some_bash_token=some_newer_value", encoding="utf-8")

        # Mock user input to choose 'y'
        with mock.patch("builtins.input", return_value="y"):
            dfm._revert_dotfiles(self.config, [self.DOTFILE_NAME])

        # Verify the newest backup was restored
        dotfile_path = self.config.output_dir / self.DOTFILE_NAME
        contents = dotfile_path.read_text(encoding="utf-8")
        assert "some_newer_value" in contents

        self.clean_up_backups()

    def test_dotfiles_not_reverted_when_arg_r_and_choice_n(self):
        """Test that dotfiles are not reverted when user chooses 'n'."""
        # Create a dotfile and backups
        self.create_dotfile()
        self.config.backups_dir.mkdir(parents=True, exist_ok=True)

        backup1 = self.config.backups_dir / f"{self.BACKUP_FILE_NAME}_2016-07-07_14-40-00.bak"
        backup2 = self.config.backups_dir / f"{self.BACKUP_FILE_NAME}_2016-07-07_14-43-00.bak"

        backup1.write_text("some_bash_token=some_value", encoding="utf-8")
        backup2.write_text("some_bash_token=some_newer_value", encoding="utf-8")

        # Mock user input to choose 'n'
        with mock.patch("builtins.input", return_value="n"):
            dfm._revert_dotfiles(self.config, [self.DOTFILE_NAME])

        # Verify the original dotfile was not changed
        dotfile_path = self.config.output_dir / self.DOTFILE_NAME
        contents = dotfile_path.read_text(encoding="utf-8")
        assert "some_newer_value" not in contents

        self.clean_up_backups()
