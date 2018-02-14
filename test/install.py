#!/usr/bin/python3

import configparser
import pathlib
import os.path

# poc install linux

def install(binary):
    config = configparser.ConfigParser()
    config['Desktop Entry'] = {
        'Name': 'testapp',
        'Exec': '.',
        'Icon': '.',
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
