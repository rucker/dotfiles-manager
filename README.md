# dotfiles

These are my dotfiles. There are many like them, but these are mine.

## Assumptions
For the Mac version, a Homebrew installation is assumed, as is using GNU Bash.

## Usage
<code>$ python ./install_dotfiles.py</code>
This will create a platform-specific bashrc/bash_profile in the project's directory as well as symlinks pointing to those files from ~). The bashrc/bash_profile is compiled from the following files:

### bash_common
Contains any elements common across platforms.

### bash_privaite (optional)
Contains any sensitive data that should not be committed to version control.

### bash_linux
Contains any elements specific to Linux.

### bash_mac
Contains any elements specific to Mac OS X.

## TO DO
- Generate template-ish bashrc/bash_profile files for display on GitHub (same as existing files, minues private info).
