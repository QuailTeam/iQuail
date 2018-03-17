"""Setup generator file."""
from distutils.core import setup

setup(
    name='quail',
    packages=['quail'],
    version='1.0',
    description='Quail cross-platform install builder',
    author='Quail team',
    author_email='quail_2020@labeip.epitech.eu',
    url='https://github.com/mouuff/Quail',
    download_url='https://github.com/mouuff/Quail/tarball/master',
    keywords=['tool', 'deploy', 'installer', 'wizard', 'install', 'update'],
    classifiers=['Intended Audience :: Developers',
                 'Development Status :: 1 - Planning',
                 'Programming Language :: Python :: 3 :: Only',
                 'Topic :: Software Development'
                 ],
    install_requires=[
        'pyinstaller', 'PyQt5'
    ],
    entry_points={
        'console_scripts': [
            'quail = quail.__main__:main'
        ]
    },
)
