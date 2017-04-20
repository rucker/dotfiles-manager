# Dotfiles Manager
Build scripts for your dotfiles!

## Purpose
Dotfiles Manager allows for the management of dotfiles across various systems. The intention is to compile your dotfiles anywhere while considering 1) the host OS and 2) any machine-specific configurations you may need.

Dotfiles are compiled line-by-line using a system of input files (more information below -- mine can be found [here](https://github.com/rucker/dotfiles/tree/master/src)).

Any existing dotfiles are backed up to $INPUT_FILES/backups automatically.

Typically, you would run `dfm.py` and provide it with your input files directory.

An example usage might be: `$ dfm.py -i ~/input-files -o ~` where:  
- `~/input-files` is the directory containing your input files
- `~` is the directory where output should be written (e.g. `.bashrc`).

See `dfm.py --help` for more.

## Supported Dofiles
Dotfiles Manager currently compiles `.bashrc/.bash_profile`, `.vimrc`, `.gitconfig`, and `.inputrc`. Support for arbitrary dotfiles of the user's choosing is planned for a future release.

## Supported Operating Systems
Linux, macOS  
I have not tested this in bash environments on Windows (e.g. Cygwin), although it might work there.

## Input Files

Each dotfile is compiled from special input files with names ending in `_global` (indicating commonality across all platforms) and `_local` (indicating specific needs of the host machine only). For most dotfiles, it's as simple as those two input files. 

The bash files (`.bashrc`/`.bash_profile`), however, require additional handling beyond the `_global` / `_local` input files because the specifics of what they do varies across operating systems and configurations.

Input files with respect to their corresponding dotfiles are described in the table below.

<table>
    <tr>
        <th>input file</th>
        <th>dotfile</th>
        <th>OS</th>
        <th>contains</th>
        <th>required?</th>
    </tr>
    <tr>
        <td>bash_global</td>
        <td>.bashrc/.bash_profile</td>
        <td>All</td>
        <td>Anything common across platforms.</td>
        <td>Y</td>
    </tr>
    <tr>
        <td>bash_local</td>
        <td>.bashrc/.bash_profile</td>
        <td>All</td>
        <td>Anything needed by the host machine only.</td>
        <td>N</td>
    </tr>
    <tr>
        <td>bash_linux</td>
        <td>.bashrc</td>
        <td>Linux</td>
        <td>Anything specific to Linux.</td>
        <td>Y*</td>
    </tr>
    <tr>
        <td>bash_mac_bsd</td>
        <td>.bash_profile</td>
        <td>macOS</td>
        <td>Anything specific to macOS systems where the BSD coreutils are used. If you're on a Mac and you're not sure what this means, you should probably use this file instead of bash_mac_gnu.</td>
        <td>Y*</td>
    </tr>
    <tr>
        <td>bash_mac_gnu</td>
        <td>.bash_profile</td>
        <td>macOS</td>
        <td>Anything specific to macOS systems where the GNU coreutils are installed.</td>
        <td>Y*</td>
    </tr>
    <tr>
        <td>gitconfig_global</td>
        <td>.gitconfig</td>
        <td>All</td>
        <td>Any parts of your .gitconfig that can be generalized across individual machines.</td>
        <td>Y</td>
    </tr>
    <tr>
        <td>vimrc_global</td>
        <td>.vimrc</td>
        <td>All</td>
        <td>Any parts of your .vimrc that can be generalized across individual machines.</td>
        <td>Y</td>
    </tr>
    <tr>
        <td>inputrc_global</td>
        <td>.inputrc</td>
        <td>All</td>
        <td>Any parts of your .inputrc that can be generalized across individual machines.</td>
        <td>Y</td>
    </tr>
</table>
*Required when actually needed (e.g. `bash_linux` is required when on Linux systems and optional otherwise).

### Precedence
Input files for each dotfile are compiled in the following order:  
1) `*_global`  
2) [`bash_linux`/`bash_mac_bsd`/`bash_mac_gnu`]  
3) `*_local`  
This means that contents of `_local` input files will be at the bottom of compiled output files. **Pay special attention to this** when writing your bash files!

## Testing  
Everything in this project is test-driven. The `test/testdriver.sh` script will run all tests.  
Unit tests: Exercise logic e.g. execution path.  
Integration tests: Deal with file IO. Runtime environment is altered so as not to break 'prod' data (the real text files).

## TODO / Wishlist
- Warn, don't error, when an expected input file is not present (don't require specific input files).  
- Compile arbitrary dotfiles using input file naming convention.
- Implement a priority-order scheme for input files compilation, e.g. rules.d style.
