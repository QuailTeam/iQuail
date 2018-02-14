#!/usr/bin/python3

import configparser
import pathlib
import os.path

# poc install linux

def install(binary):
    config = configparser.ConfigParser()
    config.optionxform=str
    config['Desktop Entry'] = {
        'Name': 'testapp',
        'Exec': '/home/mou/perso/Quail/test/install.py',
        'Icon': '/home/mou/perso/Quail/test/icon.jpeg',
        'Terminal': 'true',
        'Type': 'Application'
        }
    
    path = os.path.join(pathlib.Path.home(),
                        ".local", "share", "applications",
                        "%s.desktop" % (binary))
    with open(path, "w") as f:
        config.write(f)

if (__name__ == '__main__'):
    install("testapp")
