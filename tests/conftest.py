"""Pytest configuration and fixtures for dotfiles-manager tests."""

import shutil
import tempfile
from argparse import Namespace
from collections.abc import Generator
from pathlib import Path

import pytest

from dotfilesmanager.config import Config


@pytest.fixture
def temp_dirs() -> Generator[dict[str, Path], None, None]:
    """Create temporary directories for testing."""
    tmp_base = Path(tempfile.gettempdir()) / "dfm"
    input_dir = tmp_base / "testsrc"
    output_dir = tmp_base / "testoutputfiles"
    backups_dir = input_dir / "backups"

    # Create directories
    for directory in [tmp_base, input_dir, output_dir]:
        directory.mkdir(parents=True, exist_ok=True)

    yield {
        "base": tmp_base,
        "input": input_dir,
        "output": output_dir,
        "backups": backups_dir,
    }

    # Cleanup
    if tmp_base.exists():
        shutil.rmtree(tmp_base)


@pytest.fixture
def mock_args(temp_dirs: dict[str, Path]) -> Namespace:
    """Create mock command-line arguments for testing."""
    args = Namespace(
        input_dir=str(temp_dirs["input"]),
        output_dir=None,  # Will default to home
        clobber=False,
        revert=False,
        verbose=False,
        dry_run=False,
        file=None,
        exclude=None,
        no_symlinks=False,
    )
    return args


@pytest.fixture
def test_config(temp_dirs: dict[str, Path]) -> Config:
    """Create a test Config object with temporary directories."""
    args = Namespace(
        input_dir=str(temp_dirs["input"]),
        output_dir=[str(temp_dirs["output"])],  # Specified as list like argparse
        clobber=False,
        revert=False,
        verbose=True,  # Enable verbose for test visibility
        dry_run=False,
        file=None,
        exclude=None,
        no_symlinks=False,
    )

    # Manually create config to use test directories
    config = Config(
        input_dir=temp_dirs["input"],
        output_dir=temp_dirs["output"],
        backups_dir=temp_dirs["backups"],
        args=args,
    )

    return config
