# Dotfiles Manager
Build scripts for your dotfiles!

## Usage
`dfm.py ${INPUT_DIR}`, where `${INPUT_DIR}` is the location of your [input files](#input-files).

See `dfm.py --help` for more.

## Purpose
Dotfiles Manager allows for the management of your dotfiles across various systems while considering 1) the host OS and 2) any machine-specific configurations you may need.

Dotfiles are compiled line-by-line using a system of input files (more information [below](#input-files) -- mine can be found [here](https://github.com/rucker/dotfiles/tree/master/src)).

Existing dotfiles are backed up automatically before compilation.

## Supported Operating Systems
Linux, macOS  
I have not tested this in bash environments on Windows (e.g. Cygwin), although it might work there.

## Input Files
Each dotfile is compiled from its input file to an output file of the corresponding name (e.g. a `gitconfig` file in the input directory  will be compiled to `.gitconfig` in the output directory (`$HOME` by default)). Additional files suffixed with `_local` -- indicating specific needs of the host machine only -- will also be included. (e.g. a compiled `.gitconfig` file will include the contents of `${INPUT_DIR}/gitconfig` as well as `${INPUT_DIR}/gitconfig_local`).

#### Example Scenario
Your `gitconfig` file is under version control and it contains settings you want on any machine you use. You want to clone the file from your git repository and use it on multiple machines where you use git. However, some machines require different configurations than others (such as the git identity being used).

What this script will allow you to do is automate management of all your git configurations across all machines (including local changes). This can be done by putting the common bits in `$INPUT_DIR/gitconfig`, and the bits that vary from machine to machine in `$INPUT_DIR/gitconfig_local` as needed. Everything will then be compiled into to a single `.gitconfig` file on each machine according to your needs.

Backups will be placed in `$INPUT_DIR/backups`.

#### Bash Files
The bash dotfiles (`.bashrc`/`.bash_profile`), require additional handling beyond the naming scheme described above because the specifics of what they do varies across operating systems and configurations.

The table below explains the relationships between bash input files and output files.

<table>
    <tr>
        <th>input file</th>
        <th>dotfile</th>
        <th>OS</th>
        <th>contains</th>
    </tr>
    <tr>
        <td>bash</td>
        <td>.bashrc/.bash_profile</td>
        <td>All</td>
        <td>Anything common across platforms.</td>
    </tr>
    <tr>
        <td>bash_local</td>
        <td>.bashrc/.bash_profile</td>
        <td>All</td>
        <td>Anything needed by the host machine only.</td>
    </tr>
    <tr>
        <td>bash_linux</td>
        <td>.bashrc</td>
        <td>Linux</td>
        <td>Anything specific to Linux.</td>
    </tr>
    <tr>
        <td>bash_mac_bsd</td>
        <td>.bash_profile</td>
        <td>macOS</td>
        <td>Anything specific to macOS systems where the BSD coreutils are used. If you're on a Mac and you're not sure what this means, you should probably use this file instead of bash_mac_gnu.</td>
    </tr>
    <tr>
        <td>bash_mac_gnu</td>
        <td>.bash_profile</td>
        <td>macOS</td>
        <td>Anything specific to macOS systems where the GNU coreutils are installed.</td>
    </tr>
</table>

### Precedence
Input files for each dotfile are compiled in the following order:  
1) `$COMMON_FILE` e.g. `gitconfig` or `bash`
2) [`bash_linux`/`bash_mac_bsd`/`bash_mac_gnu`]  
3) `$LOCAL_FILE`
This means that contents of `_local` input files will be at the bottom of compiled output files. **Pay special attention to this** when writing your bash files!

## Tests
Everything in this project is test-driven. The `test/testdriver.sh` script will run all tests (Python 3.6 required).
Unit tests: Exercise logic e.g. execution path.  
Integration tests: Deal with file IO. Runtime environment is altered so as not to break 'prod' data (the real text files).

## TODO / Wishlist
- Implement a priority-order scheme for input files compilation, e.g. rules.d style.
