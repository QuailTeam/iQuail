# Quail Overview

Easy to use cross-platform installer & updater

Our goal is to make deploying and updating desktop applications as simple as possible

Today you can deploy a simple solution in less than 10 lines

Quail is currently in planning development stage, everything is subject to change

## Current features
* Install and uninstall an application on Windows and Linux (launch shortcut / uninstall registery)
* Decompress or download a solution
* Scriptable actions
* Standalone executable

## Short time goals
* Building a versionning server
* Using quail to update solutions which alerady have an installer .msi / .deb / setup.exe / .rpm  files
* Options to suggest or force updates at launch
* Integrity verification and updating only modified data
* Scriptable GUI (for install, update, uninstall)


## Installation
1. Install python 3.6
https://www.python.org/downloads/release/python-360/
2. Install Tkinter (if its not already in python3) and PyInstaller
```python -m pip install PyInstaller```

3. Run ```python setup.py install```
or set PYTHONPATH to quail directory

## Using Quail
If you find quail interesting and if you would like to use quail for your project,
feel free to contact us by email: quail_2020@labeip.epitech.eu or by creating a github issue
we will be happy to help you and make quail meet your needs.

Currently everything is subject to change, this is the main reason why there is no documentation yet,
You can still begin learning by [examples](examples)
To build a quail installer run ```quail_script.py --quail_build```


## License
This project is licensed under the Mozilla Public License 2.0 - see the [LICENSE](LICENSE) file for details

Big thanks to PyInstaller project, our project would have never been possible without them:
https://github.com/pyinstaller/pyinstaller
