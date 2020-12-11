# iQuail Overview

Easy to use cross-platform installer & updater

iQuail stands for "Installer quail"

Our goal is to make deploying and updating desktop applications as simple as possible

Today you can deploy a simple solution in less than 10 lines

iQuail is currently in development stage, everything is subject to change

## Current features
* Windows and Linux compatibility
* Install and uninstall an application (Add launch shortcut and register program on the system)
* Many ways to deploy and/or update your application:
  - Github release
  - FTP server
  - Embedded in installer (offline installer)
* Graphical user interface
* Scriptable user interface
* Configuration management
* Custom scriptable install/uninstall actions
* Configurable "Force update" or "Ask for update"


## Installation
1. Install python 3.6
https://www.python.org/downloads/release/python-360/
2. Install Tkinter (if its not already in python3) on debian/ubuntu:
```sudo apt-get install python3-tk``` on fedora ```sudo dnf install python3-tk```
3. Install iQuail
```python3 -m pip install iQuail```


## Using iQuail
Currently everything is subject to change,

You can still begin learning by [examples](examples)

To build a iQuail installer run ```iquail_script.py --iquail_build```

How to sign? https://github.com/pyinstaller/pyinstaller/wiki/Recipe-Win-Code-Signing

## Short time goals
* Integrity verification and updating only modified data
* Building a versioning server
* Using iquail to update solutions which already have an installer .msi / .deb / setup.exe / .rpm  files
* Mac OS support

## Support
If you find iquail interesting and if you would like to use iquail for your project,
feel free to contact us by email: quail_2020@labeip.epitech.eu or by creating a github issue
we will be happy to help you and make iquail meet your needs.


## License
This project is licensed under the Mozilla Public License 2.0 - see the [LICENSE](LICENSE) file for details

Big thanks to PyInstaller project, our project would have never been possible without them:
https://github.com/pyinstaller/pyinstaller
