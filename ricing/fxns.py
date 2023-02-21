#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Provide common functions for other objects."""
from os import sep
from pathlib import Path
from subprocess import run, PIPE
from shlex import split
from pkg_resources import resource_filename

from ricing import RICE_DB_PATH, RICE_CONFIG_DB
from ricing.sql import create_rice_db
from ricing.settings import DEFAULT_ENC


def capture_cmd(cmd: str, strip: bool = True) -> str:
    """Execute cmd in a subprocess.run call and return the output.
    Args:
        cmd: the full command to be run in a subprocess.run call
    """
    result = run(split(cmd), stdout=PIPE, stderr=PIPE, shell=True, text=True)
    if strip is True:
        return result.stdout.strip()
    return result.stdout


def which_output(cmd: str) -> str:
    """Check the location of a command."""
    result = run(['which', cmd], stdout=PIPE, stderr=PIPE, shell=True,
                 text=True)
    return result.stdout.strip()


def safe_db_creation(
    db_path: Path = RICE_DB_PATH,
    conn_str: str = RICE_CONFIG_DB,
    overwrite: bool = False, **kwargs
):
    """Initialize the rice database."""
    if db_path.exists() and overwrite is True:
        create_rice_db(connection_str=conn_str)


def load_pkg_data(file: str, encoding: str = DEFAULT_ENC):
    """Load a pkg data file."""
    return Path(resource_filename('ricing', 'data' + sep + file)).read_text(
        encoding=encoding,
    )
