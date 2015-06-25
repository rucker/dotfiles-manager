# dotfiles

These are my dotfiles. There are many like them, but these are mine.

## Background
My dotfiles reached a point where they became complex enough that I didn't want to manage them by hand any more. Not only do I want different things in .bashrc on Linux than I do in .bash_profile on OS X, but I also want to avoid accidentally committing any sensitive data they might contain to GitHub.

To that end, I wrote a Python script that will compile these files (.bashrc and .bash_profile for Linux and OS X, respectively) from external files (below) and generate the appropriate symlinks in ~.

## Usage
<code>$ python ./dotfilesinstaller.py</code>
This will create a platform-specific bashrc/bash_profile in the project's directory as well as symlinks pointing to those files from ~). The bashrc/bash_profile is compiled from the following files:

### bash_common
Contains any elements common across platforms.

### bash_privaite (optional)
Contains any sensitive data that should not be committed to version control.

### bash_linux
Contains any elements specific to Linux.

### bash_mac
Contains any elements specific to Mac OS X.

## Assumptions
For the Mac version, a Homebrew installation is assumed as is using GNU Bash.
