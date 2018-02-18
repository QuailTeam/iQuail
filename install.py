#!/usr/bin/python3


import os
import os.path
import quail

solution_path = os.path.join(os.getcwd(), 'test_solution')

print(solution_path)

config = {
    'name': 'LolAllum1',
    'icon': 'icon.jpeg',
    'binary': 'allum1',
    'solution_path': solution_path,
    'console': True
}

installer = quail.LinuxInstaller(**config)

installer.install()

