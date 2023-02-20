#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The ricing module provides an easy infrastructure for the creation and
   distribution of ricing configs across a system.
"""
from pathlib import Path
from os import getenv, sep
_CONFIG_DIR = '.config'
_RICE_DIR = 'rice'
_RICE_DB = 'rice.db'
_RICE_DB_TYPE = 'sqlite'

RICE_CONFIG_DIR = f'{_CONFIG_DIR}{sep}{_RICE_DIR}{sep}'
RICE_CONFIG_DB = f'{_RICE_DB_TYPE}://{RICE_CONFIG_DIR}{_RICE_DB}'
RICE_HOME = (Path(getenv('HOME')).resolve() / _CONFIG_DIR) / _RICE_DIR
RICE_DB = RICE_HOME / _RICE_DB
