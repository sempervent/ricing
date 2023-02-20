#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Provide common functions for other objects."""
from pathlib import Path
from subprocess import run, PIPE

from ricing import RICE_DB
from ricing.sql import SCHEMA_QUERY


def capture_cmd(cmd: str) -> str:
    """Execute cmd in a subprocess.run call and return the output."""
    result = run(cmd, stdout=PIPE, stderr=PIPE, shell=True, text=True)
    return result.stdout


def create_rice_db(db_path: Path = RICE_DB, overwrite: bool = False):
    """Initialize the rice database."""
    if db_path.exists() and overwrite is True:

