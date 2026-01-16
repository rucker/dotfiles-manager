# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Dotfiles Manager is a Python tool that compiles dotfiles from multiple source files, enabling users to maintain both global (version-controlled) and local (machine-specific) configurations. It supports priority-based file merging, automatic backups, and symlink creation.

## Development Commands

### Installation

```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install in editable mode with dev dependencies
python -m pip install -e .[dev]
```

**Note:** A `.venv` directory will be created (already in `.gitignore`). Always activate the venv before running commands.

### Running Tests

```bash
# Run all tests with coverage
pytest

# Run specific test file
pytest tests/test_dotfilesmanager.py

# Run with verbose output
pytest -v

# Generate coverage report
pytest --cov=dotfilesmanager --cov-report=html
```

### Running the Tool

```bash
# After installation
dfm <input_dir> [options]

# Or run as module
python -m dotfilesmanager.dfm <input_dir> [options]
```

Common options:
- `-v, --verbose` - Enable verbose output
- `-o, --output-dir <dir>` - Specify output directory (default: $HOME)
- `-f, --file <name>` - Process only the specified dotfile
- `-e, --exclude <file>` - Exclude specific input files
- `-r, --revert` - Revert dotfiles to most recent backup
- `-c, --clobber` - Don't back up existing files
- `--dry-run` - Show what would happen without making changes (implies -v)
- `--no-symlinks` - Compile files instead of creating symlinks

### Code Quality

```bash
# Format code
black dotfilesmanager/ tests/

# Sort imports
isort dotfilesmanager/ tests/

# Type check
mypy dotfilesmanager/

# Lint
ruff check dotfilesmanager/ tests/
```

### Building

```bash
# Build wheel
python -m pip install build
python -m build

# Verify wheel
ls -lh dist/
```

## Architecture

### Module Structure

The codebase uses **dependency injection** via the `Config` dataclass for sharing configuration across components:

- **`dotfilesmanager/dfm.py`** - Main entry point and orchestration
  - CLI argument parsing and validation
  - Creates `Config` object from parsed arguments
  - Coordinates the compilation process
  - Implements dotfile naming convention logic (`_get_dotfile_name`, `_sort_input_file_list`)
  - All functions accept `config: Config` parameter

- **`dotfilesmanager/config.py`** - Configuration dataclass
  - `Config` dataclass stores: `input_dir`, `output_dir`, `backups_dir`, `args`
  - `Config.from_args()` - Factory method to create Config from argparse Namespace
  - Properties: `verbose`, `dry_run`, `clobber` - Convenient access to arg flags
  - Validates directories exist and are different

- **`dotfilesmanager/ioutils/ioutils.py`** - File I/O operations
  - All functions accept `config: Config` as first parameter
  - `compile_dotfile(config, ...)` - Merges multiple input files into one output file
  - `create_symlink(config, ...)` - Creates symlinks for single-input dotfiles
  - `revert_dotfile(config, ...)` - Restores from backup (interactive)
  - `_back_up(config, ...)` - Creates timestamped backups before overwriting
  - `prints(config, ...)` and `printe(...)` - Verbose and error output

### Input File Naming Convention

Input files follow the pattern: `[XX-]dotfile[.ext][_suffix]`

- `XX-` (optional) = Priority number (99 is highest, processed first; files are reverse-sorted by priority)
- `dotfile` = Output dotfile name (leading dot is added automatically)
- `.ext` (optional) = Extension for output file (e.g., `tmux.conf`)
- `_suffix` (optional) = Ignored suffix for organizing input files

**Examples:**
- `bashrc` → `.bashrc`
- `99-bashrc`, `bashrc_local` → `.bashrc` (merged with 99-bashrc content first)
- `gitconfig` → `.gitconfig`
- `98-bashrc_linux`, `bashrc_local.myaliases` → `.bashrc`

**Important:** Any extension appearing after an underscore is considered part of the suffix and ignored.

### Compilation Logic

1. **Single input file** → Creates symlink to input file (unless `--no-symlinks`)
2. **Multiple input files** → Compiles content into a single output file
   - Files with priority numbers (e.g., `99-`) are processed first (reverse sorted)
   - Other files are processed in lexicographical order
   - All content is concatenated into the output dotfile

### Backup System

- Backups are created in `${INPUT_DIR}/backups/` before overwriting existing files
- Backup filename format: `dotfile_YYYY-MM-DD_HH-MM-SS.bak` (leading dot removed)
- If a dotfile is a symlink, its target is backed up
- Revert operation (`-r`) finds the most recent backup by timestamp

### Testing Structure

Tests use `pytest` framework with fixtures:
- `tests/test_dotfilesmanager.py` - Unit tests for main orchestration logic
- `tests/test_dotfilesmanager_int.py` - Integration tests for dfm.py
- `tests/test_ioutils.py` - Unit tests for I/O utilities
- `tests/test_ioutils_int.py` - Integration tests for file operations
- `tests/conftest.py` - Pytest fixtures providing test configuration and temporary directories

**Key fixtures:**
- `test_config` - Provides a `Config` object configured for testing with temp directories
- `temp_dirs` - Provides temporary input/output/backup directories
- Both fixtures handle setup and automatic cleanup

## Key Implementation Details

### Dependency Injection Pattern
The codebase uses dependency injection to pass configuration through function calls:
- All functions accept a `config: Config` parameter as their first argument
- `Config` is a dataclass containing all necessary configuration state
- This pattern makes code testable without global state
- In tests: Fixtures create `Config` objects with test-specific settings
- Type hints ensure compile-time safety for configuration access

### Symlink Handling
When creating symlinks, the code:
- Checks if target already exists and is correct (no-op if so)
- Backs up broken symlinks before removing them
- Dereferences symlinks when backing up (backs up the target, not the link itself - see issue #57)

### File Processing
Input files must be UTF-8 encoded. Non-UTF-8 files are skipped with a warning during compilation.
