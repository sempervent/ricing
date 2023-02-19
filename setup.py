#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The ricing module allows for quick setup and sharing of user environment
   settings by storing configuration files in a hidden user directory database.
   The configuration can be saved or chosen via the command line.
"""
from pathlib import Path
from re import sub as resub
from sys import modules

from setuptools import setup, find_packages


_HERE = Path(__file__).resolve().parent
_ek = {'encoding': 'utf-8'}
_url = f'https://github.com/sempervent/{_HERE.name}.git'


def _strip(file_name: str):
    """Strip text from a file."""
    return (_HERE / file_name).read_text(**_ek).strip()


_SETUP = {
    'name': _HERE.name,
    'version': _strip('VERSION'),
    'description': resub(r'\s+', ' ', modules[__name__].__doc__),
    'long_description': _strip('README.md'),
    'long_description_content_type': 'text/markdown',
    'url': _url,
    'author': 'Joshua N. Grant',
    'author_email': 'jngrant@live.com',
    'packages': find_packages(exclude=['tests', 'scripts']),
    'classifiers': [
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Programming Lagunage :: Python 3.7",
        "Programming Lagunage :: Python 3.8",
        "Programming Lagunage :: Python 3.9",
        "Programming Lagunage :: Python 3.10",
        "Programming Lagunage :: Python 3.11",
        "Topic :: Desktop Environment :: Customization",
        "Topic :: System :: Filesystems",
        "Topic :: Database :: Front-Ends",
    ],
    'install_requires': _strip('requirements.txt').split(),
}

print(_SETUP)