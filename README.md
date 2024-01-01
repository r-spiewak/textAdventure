# About textAdventureRGS

This is a simple text adventure game built in Python using class objects.

The source code is included in the distribution, but if you wish to play the example game, please do not peek. 
<!--A map of the included game is also available upon request. However, this will really spoil the fun.-->

## Requirements:
- Python
- Git
- Some kind of terminal emulator

## Installation

This can be installed using the Python package installer `pip` (a suitable version of Python must already be installed prior to using `pip`):

Windows (do not include the leading '`C:>`'):
```
C:> py -m pip install -e "git+https://github.com/r-spiewak/textAdventure/#egg=textAdventurergs3"
```

Linux and Mac (do not include the leading '`$`'):
```
$ python -m pip install -e "git+https://github.com/r-spiewak/textAdventure/#egg=textAdventurergs3"
```
<!--
Mac:
```
$ python -m pip install -e "vcs+protocol://repo_url/#egg=pkg&subdirectory=pkg_dir"
https://github.com/r-spiewak/textAdventure/#egg=textAdventureRGS3&subdirectory=pkg_dir
```
-->

*Note: it may be neccessary to run `python3` instead of `python`, depending upon your version of Python.*

Android:
You need to install a terminal, `git`, and a suitable Python interpreter. Try the Termux (I have no affiliation with the app, but I was able to correctly install everything from it) app, from which you can run the following (the `$` on each line is the prompt in the terminal, not something you should enter):
```
$ apt-get update
$ apt-get upgrade
$ apt-get install git
$ apt-get install python
$ pip install -e "git+https://github.com/r-spiewak/textAdventure/#egg=textAdventureRGS3"
```

*Note: you may get warnings about unsigned packages. I installed them anyway, since without them this won't work, but I cannot and do not in any way guarantee their safety or security.*

## Running the Example

After installation (see above), the example should be runnable with the following command line interface (cli):
```
textAdventure
```

# License
    textAdventureRGS3: a simple framework for a simple text adventure game, mostly created for fun for the included example.
    Copyright (C) 2022  Russell Spiewak

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
