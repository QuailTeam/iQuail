# Quail Overview
[![Build Status](https://travis-ci.org/QuailTeam/Quail.svg?branch=master)](https://travis-ci.org/QuailTeam/Quail)

Easy to use cross-platform installer & updater

Our goal is to make deploying and updating desktop applications as simple as possible

Today you can deploy a simple solution in less than 10 lines

Quail is currently in planning development stage, everything is subject to change

## Current features
* Install and uninstall an application on Windows and Linux (Add launch shortcut and register program on the system)
* Decompress or download a solution
* Building standalone offline installer
* Building installer which uses github release feature to deploy/update solutions
* Tkinter user interface
* Scriptable actions

## Installation
1. Install python 3.6
https://www.python.org/downloads/release/python-360/
2. Install Tkinter (if its not already in python3)
3. Install PyInstaller
```python3 -m pip install PyInstaller```

4. Run ```python3 setup.py install``` OR set PYTHONPATH to quail directory

## Using Quail
Currently everything is subject to change, this is the main reason why there is no documentation yet,

You can still begin learning by [examples](examples)

To build a quail installer run ```quail_script.py --quail_build```

## Short time goals
* Integrity verification and updating only modified data
* Building a versioning server
* Using quail to update solutions which already have an installer .msi / .deb / setup.exe / .rpm  files
* Scriptable GUI (for install, update, uninstall)
* Mac OS support

## Support
If you find quail interesting and if you would like to use quail for your project,
feel free to contact us by email: quail_2020@labeip.epitech.eu or by creating a github issue
we will be happy to help you and make quail meet your needs.


## License
This project is licensed under the Mozilla Public License 2.0 - see the [LICENSE](LICENSE) file for details

Big thanks to PyInstaller project, our project would have never been possible without them:
https://github.com/pyinstaller/pyinstaller
