#!/usr/bin/python3

import os
import os.path
import iquail
import platform

if iquail.helper.OS_LINUX:
    solution_path = ['Allum1']
    iquail.run(
        iquail.SolutionLocal(['Allum1']),
        iquail.Installer(
            name='Allum1',
            icon='icon.jpeg',
            binary='allum1',
            console=True,
            install_systemwide=False,
            linux_exec_flags='%f',
            linux_desktop_conf={
                'Categories': 'GNOME;GTK;Utility;TextEditor;Development;',
                'MimeTypes': 'text/plainimage/bmp;image/g3fax;image/gif;image/x-fits;image/x-pcx;image/x-portable'
                             '-anymap;image/x-portable-bitmap;image/x-portable-graymap;image/x-portable-pixmap;image'
                             '/x-psd;image/x-sgi;image/x-tga;image/x-xbitmap;image/x-xwindowdump;image/x-xcf;image/x'
                             '-compressed-xcf;image/x-gimp-gbr;image/x-gimp-pat;image/x-gimp-gih;image/tiff;image'
                             '/jpeg;image/x-psp;application/postscript;image/png;image/x-icon;image/x-xpixmap;image'
                             '/svg+xml;application/pdf;image/x-wmf;image/jp2;image/jpeg2000;image/jpx;image/x-xcursor'
                             ';',
                'Comment': 'best game ever'
            }
        ),
        iquail.builder.Builder(
            iquail.builder.CmdIntegrity(solution_path)
        )
    )
if iquail.helper.OS_WINDOWS:
    solution_path = ['OpenHardwareMonitor']
    iquail.run(
        iquail.SolutionLocal(['OpenHardwareMonitor']),
        iquail.Installer(
            name='OpenHardwareMonitor',
            icon='OpenHardwareMonitor.exe',
            binary='OpenHardwareMonitor.exe',
            console=True
        ),
        iquail.builder.Builder(
            iquail.builder.CmdIntegrity(solution_path)
        )
    )
