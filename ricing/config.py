#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Describe a *Config objects."""
from datetime import datetime
from pathlib import Path
from pydantic import BaseModel

from ricing import RICE_HOME
from ricing.fxns import capture_cmd


class BaseConfig(BaseModel):
    """A BaseConfig object."""
    created_at: datetime = datetime.now()  # create the config now
    system_user: str = capture_cmd('whoami')  # whoami?
    home: Path = RICE_HOME  # the directory where rice homing belongs
