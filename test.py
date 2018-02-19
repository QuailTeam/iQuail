#!/usr/bin/python3


import os
import os.path
import quail

solution_path = os.path.join(os.getcwd(), 'test_solution')

config = {
    'name': 'LolAllum1',
    'icon': 'icon.jpeg',
    'binary': 'allum1',
    'solution_path': solution_path,
    'console': True
}

quail.run(config)


