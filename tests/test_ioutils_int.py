"""Integration tests for dotfilesmanager.ioutils.ioutils module."""

import io

import pytest

from dotfilesmanager import dfm
from dotfilesmanager.ioutils import ioutils


class TestIOUtilsInt:
    """Integration tests for I/O utility functions."""

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

    def test_existing_dotfile_backed_up_when_not_arg_c(self):
        """Test that existing dotfiles are backed up when overwritten."""
        self.create_dotfile()
        self.config.backups_dir.mkdir(parents=True, exist_ok=True)

        with io.StringIO() as buf:
            buf.write("some_bash_token=some_newer_value")
            ioutils._write_output_file(
                self.config, str(self.config.output_dir / self.DOTFILE_NAME), buf
            )

        backup_files = list(self.config.backups_dir.glob("*.bak"))
        assert len(backup_files) == 1

        backup_content = backup_files[0].read_text(encoding="utf-8")
        assert "some_value" in backup_content

        self.clean_up_backups()

    def test_output_file_contains_all_input_files_in_correct_order(self):
        """Test that compiled dotfile contains all input files in priority order."""
        line_1 = "first-token\n"
        line_2 = "second-token\n"
        line_3 = "third-token\n"

        (self.config.input_dir / self.FIRST_INPUT_FILE).write_text(line_1, encoding="utf-8")
        (self.config.input_dir / self.SECOND_INPUT_FILE).write_text(line_2, encoding="utf-8")
        (self.config.input_dir / "fooconfig").write_text(line_3, encoding="utf-8")

        dotfiles_dict = dfm._get_dotfiles_dict(self.config)
        dfm._process_dotfiles(self.config, dotfiles_dict)

        output_file = self.config.output_dir / self.DOTFILE_NAME
        file_contents = output_file.read_text(encoding="utf-8").splitlines(keepends=True)
        assert file_contents[0] == line_1

        self.clean_up_backups()
        (self.config.input_dir / "fooconfig").unlink()

    def test_when_arg_e_then_specified_file_is_excluded(self):
        """Test that files specified with -e are excluded from compilation."""
        self.config.args.exclude = [[self.SECOND_INPUT_FILE]]

        (self.config.input_dir / self.FIRST_INPUT_FILE).write_text(
            "some_token=some_value", encoding="utf-8"
        )
        (self.config.input_dir / self.SECOND_INPUT_FILE).write_text(
            "some_local_token=some_value", encoding="utf-8"
        )
        (self.config.input_dir / "fooconfig").write_text(
            "some_additional_token=some_value", encoding="utf-8"
        )

        dotfiles_dict = dfm._get_dotfiles_dict(self.config)
        dfm._process_dotfiles(self.config, dotfiles_dict)

        output_content = (self.config.output_dir / self.DOTFILE_NAME).read_text(encoding="utf-8")
        first_input_content = (self.config.input_dir / self.FIRST_INPUT_FILE).read_text(
            encoding="utf-8"
        )
        second_input_content = (self.config.input_dir / self.SECOND_INPUT_FILE).read_text(
            encoding="utf-8"
        )

        assert first_input_content in output_content
        assert second_input_content not in output_content

    def test_backing_up_file_removes_original(self):
        """Test that backing up a file removes the original."""
        dotfile_path = self.config.output_dir / self.DOTFILE_NAME
        dotfile_path.write_text("some_token=some_value", encoding="utf-8")

        self.config.backups_dir.mkdir(parents=True, exist_ok=True)
        ioutils._back_up(self.config, str(dotfile_path))

        assert not dotfile_path.exists()

    def test_compile_nested_dotfile_creates_parent_dirs(self):
        """Test that compiling a nested dotfile creates parent directories."""
        # Create nested input file
        nested_input_dir = self.config.input_dir / ".config" / "nvim"
        nested_input_dir.mkdir(parents=True, exist_ok=True)
        (nested_input_dir / "init.vim").write_text("set number\n", encoding="utf-8")

        # Compile the nested dotfile
        output_path = str(self.config.output_dir / ".config/nvim/init.vim")

        with io.StringIO() as buf:
            buf.write("set number\n")
            ioutils._write_output_file(self.config, output_path, buf)

        # Check that the output file exists
        output_file = self.config.output_dir / ".config" / "nvim" / "init.vim"
        assert output_file.exists()
        assert output_file.read_text(encoding="utf-8") == "set number\n"

    def test_symlink_nested_file_creates_parent_dirs(self):
        """Test that creating a symlink for nested file creates parent directories."""
        # Create nested input file
        nested_input_dir = self.config.input_dir / ".config" / "nvim"
        nested_input_dir.mkdir(parents=True, exist_ok=True)
        input_file = nested_input_dir / "init.vim"
        input_file.write_text("set number\n", encoding="utf-8")

        # Create symlink
        target = str(input_file)
        source = str(self.config.output_dir / ".config" / "nvim" / "init.vim")

        ioutils.create_symlink(self.config, target, source)

        # Check that parent directories were created
        assert (self.config.output_dir / ".config" / "nvim").exists()
        assert (self.config.output_dir / ".config" / "nvim" / "init.vim").is_symlink()

    def test_backup_nested_file_preserves_structure(self):
        """Test that backing up a nested file preserves directory structure."""
        # Create nested dotfile in output directory
        nested_output = self.config.output_dir / ".config" / "nvim"
        nested_output.mkdir(parents=True, exist_ok=True)
        dotfile_path = nested_output / "init.vim"
        dotfile_path.write_text("old config\n", encoding="utf-8")

        # Back up the file
        self.config.backups_dir.mkdir(parents=True, exist_ok=True)
        ioutils._back_up(self.config, str(dotfile_path))

        # Check that backup preserves structure
        backup_files = list(self.config.backups_dir.glob("config/nvim/init.vim_*.bak"))
        assert len(backup_files) == 1
        assert backup_files[0].read_text(encoding="utf-8") == "old config\n"
        assert not dotfile_path.exists()

        self.clean_up_backups()

    def test_revert_nested_file(self):
        """Test that reverting a nested file works correctly."""
        # Create nested backup
        backup_dir = self.config.backups_dir / "config" / "nvim"
        backup_dir.mkdir(parents=True, exist_ok=True)
        backup_file = backup_dir / "init.vim_2024-01-01_12-00-00.bak"
        backup_file.write_text("backup content\n", encoding="utf-8")

        # Revert the file (simulating user input "Y")
        import unittest.mock as mock

        with mock.patch("builtins.input", return_value="Y"):
            ioutils.revert_dotfile(self.config, ".config/nvim/init.vim")

        # Check that the file was restored
        restored_file = self.config.output_dir / ".config" / "nvim" / "init.vim"
        assert restored_file.exists()
        assert restored_file.read_text(encoding="utf-8") == "backup content\n"

        self.clean_up_backups()
