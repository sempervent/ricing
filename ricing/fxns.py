#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Provide common functions for other objects."""
from pathlib import Path
from subprocess import run, PIPE
from shlex import split

from ricing import RICE_CONFIG_DB
from ricing.sql import create_rice_db


def capture_cmd(cmd: str, strip: bool = True) -> str:
    """Execute cmd in a subprocess.run call and return the output.
    Args:
        cmd: the full command to be run in a subprocess.run call
    """
    result = run(split(cmd), stdout=PIPE, stderr=PIPE, shell=True, text=True)
    if strip is True:
        return result.stdout.strip()
    return result.stdout


def safe_db_creation(
    db_path: Path = RICE_CONFIG_DB, overwrite: bool = False, **kwargs
):
    """Initialize the rice database."""
    if db_path.exists() and overwrite is True:
        create_rice_db()
