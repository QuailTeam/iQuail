"""Setup generator file."""
from setuptools import setup, find_packages
import sys

with open("README.md", "r") as f:
    long_description = f.read()

requirements = open("requirements.txt").read().splitlines()
packages = find_packages()
packages.remove("tests")

setup(
    name='iquail',
    packages=packages,
    version='1.9',
    description='iQuail cross-platform installer',
    author='Quail team',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author_email='quail_2020@labeip.epitech.eu',
    url='https://github.com/QuailTeam/iQuail',
    keywords=['tool', 'deploy', 'installer', 'wizard', 'install', 'update', 'quail'],
    classifiers=['Intended Audience :: Developers',
                 'Development Status :: 4 - Beta',
                 'Programming Language :: Python :: 3 :: Only',
                 'Topic :: Software Development'
                 ],
    install_requires=requirements,
    include_package_data=True
)
