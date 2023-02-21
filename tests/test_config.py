"""Test the Config objects."""
from uuid import UUID
from os import environ, getenv
from datetime import datetime
from pathlib import Path

import pytest

from ricing import RICE_HOME
from ricing.config import (
    convert_str_to_path,
    PathNameUUID,
    Program,
    Config,
)


@pytest.mark.parametrize(
    "pathstr",
    ['folders.py', 'this/string/has/folders.py', '/this/absolute/path.py', '.', '~/.vimrc',
     '~/.config'])
def test_convert_str_to_path(pathstr):
    """Test conversion of a string to path."""
    path = convert_str_to_path(path=pathstr)
    assert isinstance(path, Path)
    add = 1
    if pathstr.startswith('/') or pathstr == '.':
        add = 0
    if pathstr.startswith('~'):
        assert getenv('HOME') in str(path)
        return
    assert len(path.parents) == pathstr.count('/') + add


@pytest.mark.parametrize(
    "path",
    ['folders.py', Path('/dev/null'), Path('/etc/os-release'),
     '~/.vimrc', '~/.bashrc'])
def test_PathNameUUID(path):
    """Test that the PathNameUUID object works as expected."""
    pnu = PathNameUUID(name='pnu', path=path)
    assert isinstance(pnu.path, Path)
    assert isinstance(pnu.id, UUID)
    assert isinstance(pnu.get_id(), str)
    assert isinstance(pnu.use_bytes, bool)
    assert pnu.encoding == 'utf-8'
    if pnu.path.is_file():
        assert isinstance(pnu.contents(), str)
    pnu.use_bytes = True
    if pnu.path.is_file():
        assert isinstance(pnu.contents(), bytes)


def test_Program():
    """Test that the Program object works as expected."""
    p = Program(name='vim', path='/bin/vim', executable='vim',
                config_path='~/.vimrc')
    assert isinstance(p.path, Path)
    assert isinstance(p.id, UUID)


def test_Config():
    """Test the BaseConfig class."""
    bc = Config()
    # created at should be a datetime object
    assert isinstance(bc.created_at, datetime)
    assert bc.system_user == environ['USER']
    # test the str, as magic happens to the classes
    assert isinstance(bc.home, Path)
    assert str(bc.home.resolve()) == str(RICE_HOME.resolve())
    assert str(bc.home) == environ['HOME'] + '/.config/rice'
    if bc.home.exists():  # if the directory exists, ensure it is the same
        assert bc.home.samefile(RICE_HOME)  # not run if directory nonexistent
