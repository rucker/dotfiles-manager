"""Configuration management for dotfiles manager."""

import os
import sys
from argparse import Namespace
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Config:
    """Configuration for dotfiles manager operations."""

    input_dir: Path
    output_dir: Path
    backups_dir: Path
    args: Namespace

    @classmethod
    def from_args(cls, args: Namespace) -> "Config":
        """Create Config from parsed arguments."""
        input_dir = Path(args.input_dir)

        # Validate input directory exists
        if not input_dir.is_dir():
            print(f"Specified input directory {input_dir} does not exist.", file=sys.stderr)
            sys.exit(1)

        # Determine output directory
        if args.output_dir:
            output_dir = Path(args.output_dir[0])
        else:
            output_dir = Path.home()

        # Validate input and output are different
        if input_dir == output_dir:
            print(
                f"INPUT_DIR {input_dir} cannot be the same as OUTPUT_DIR {output_dir}",
                file=sys.stderr,
            )
            sys.exit(1)

        backups_dir = input_dir / "backups"

        return cls(
            input_dir=input_dir,
            output_dir=output_dir,
            backups_dir=backups_dir,
            args=args,
        )

    @property
    def verbose(self) -> bool:
        """Check if verbose mode is enabled."""
        return self.args.verbose or self.args.dry_run

    @property
    def dry_run(self) -> bool:
        """Check if dry-run mode is enabled."""
        return self.args.dry_run

    @property
    def clobber(self) -> bool:
        """Check if clobber mode is enabled."""
        return self.args.clobber
