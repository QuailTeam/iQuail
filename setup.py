"""Setup generator file."""
from distutils.core import setup

setup(
    name='quail',
    packages=['quail'],
    version='1.0',
    description='Quail cross-platform install builder',
    author='Quail team',
    author_email='arnaudalies.py@gmail.com',
    url='https://github.com/mouuff/Quail',
    download_url='https://github.com/mouuff/Quail/tarball/master',
    keywords=['tool', 'deploy', 'installer', 'wizard', 'install'],
    classifiers=[],
    install_requires=[
        'pyinstaller'
    ],
    entry_points={
        'console_scripts': [
            'quail = quail.__main__:main'
        ]
    },
)
