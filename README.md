# dotfiles
These are my dotfiles. There are many like them, but these are mine.

## Background
My dotfiles reached a point where they became complex enough that I didn't want to manage them by hand any more. Not only do I want different things in .bashrc on Linux than I do in .bash_profile on OS X, but I also want to avoid accidentally committing any sensitive data they might contain to GitHub.

To that end, I wrote a Python script that will compile these dotfiles from external files (below) and generate the appropriate symlinks in ~ .

## Usage
<code>$ python ./scripts/dotfilesinstaller.py</code>
This will create a platform-specific bash dotfile in the project's directory as well as symlinks pointing to those files from ~/ . The dotfiles are compiled from the following files, which are located in the <code>inputfiles</code> directory:

### bash_common
Contains any elements common across platforms.

### bash_private (optional)
Contains any sensitive data that should not be committed to version control.

### bash_linux
Contains any elements specific to Linux.

### bash_mac
Contains any elements specific to Mac OS X.

## Testing
A suite of unit tests is included in test_dotfiles.py. To run this, the <code>mock</code> package is required. Fetch it from PyPi using pip, i.e. <code>$ pip install mock</code>

## Assumptions
For the Mac version, a Homebrew installation is assumed as is using GNU Bash.

## FAQ
**Q**: The script creates bashrc/bash_profile and .bashrc/.bash_profile. Why two versions of each?  
**A**: bashrc/bash_profile are what I commit to GitHub. They are for show. These files do not contain the contents of bash_private, whereas their dotted counterparts (which are what gets symlinked to from ~) do contain those private tokens.

## TO DO  
-Nothing for now!
