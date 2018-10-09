"""Setup generator file."""
from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

requirements = open("requirements.txt").read().splitlines()

setup(
    name='quail',
    packages=['quail'],
    version='1.2',
    description='Quail cross-platform installer',
    author='Quail team',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author_email='quail_2020@labeip.epitech.eu',
    url='https://github.com/QuailTeam/Quail',
    keywords=['tool', 'deploy', 'installer', 'wizard', 'install', 'update'],
    classifiers=['Intended Audience :: Developers',
                 'Development Status :: 3 - Alpha',
                 'Programming Language :: Python :: 3 :: Only',
                 'Topic :: Software Development'
                 ],
    install_requires=[
        'pyinstaller'
    ],
)
