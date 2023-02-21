#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Describe a *Config objects."""
from os import getenv
from uuid import uuid4, UUID
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Union

from pydantic import BaseModel, validator

from ricing import RICE_HOME
from ricing.fxns import capture_cmd
from ricing.db import RiceDB
from ricing.settings import DEFAULT_ENC


def convert_str_to_path(path: Union[Path, str]) -> Path:
    """Convert a str to a path."""
    if isinstance(path, str):
        if '~' in path:
            path = path.replace('~', getenv('HOME'))
        path = Path(path)
    return path


class PathNameUUID(BaseModel):
    id: UUID = uuid4()
    name: str
    path: Union[Path, str]
    use_bytes: bool = False
    encoding: str = DEFAULT_ENC

    @validator('path')
    def _path_validator(cls, path: Union[Path, str]) -> Path:
        """Ensure path is a Path object."""
        return convert_str_to_path(path=path)

    def get_id(self):
        """Get the id of the object as a string."""
        return str(self.id)

    def contents(self):
        """Retrieve the contents of the file."""
        if self.use_bytes is True:
            return self.path.read_bytes()
        return self.path.read_text(encoding=self.encoding)


class Program(PathNameUUID):
    """Configure a Program for a rice by associating it with a config file."""
    executable: str
    config_path: Union[Path, str]

    @validator('config_path')
    def _config_path_validator(cls, config_path: Union[Path, str]) -> Path:
        """Convert a config path to a Path."""
        return convert_str_to_path(path=config_path)


class File(PathNameUUID):
    """Configure a File for a rice."""
    program: Program
    encoding: str = DEFAULT_ENC
    use_bytes: bool = False

    def contents(self):
        """Retrieve the contents of the file."""
        if self.use_bytes is True:
            return self.path.read_bytes()
        return self.path.read_text(encoding=self.encoding)


class RiceConfig(BaseModel):
    """Configure a rice."""
    id: uuid4 = uuid4()
    name: str
    files: Optional[List[File]] = None
    programs: Optional[List[Program]] = None

    def add_file(
        self, file: File | None = None, files: List[File] | None = None
    ):
        """Add a file to the files object."""
        if isinstance(file, File):
            if self.files is None:
                self.files = [file]
            elif isinstance(self.files, list):
                self.files.append(file)
            elif isinstance(self.files, File):
                self.files = [self.files, file]
        if all([isinstance(f, File) for f in files]):
            if self.files is None:
                self.files = files
            elif isinstance(self.files, list):
                self.files.extend(files)
            elif isinstance(self.files, File):
                self.files = [self.files] + files


class Config(BaseModel):
    """A BaseConfig object."""
    created_at: datetime = datetime.now()  # create the config now
    system_user: str = capture_cmd('whoami')  # whoami?
    home: Path = RICE_HOME  # the directory where rice homing belongs
    db: RiceDB = RiceDB()
    # below are set by internal methods, but can be set on initialization
    configs: Optional[List[RiceConfig]] = None

    def add_config(self, config: RiceConfig):
        """Add a RiceConfig to the system configuration."""
        if not isinstance(config, RiceConfig):
            raise TypeError(f'{config} object is not of type RiceConfig')
        if self.configs is None:
            self.configs = [config]
        elif isinstance(self.configs, list):
            self.configs.append(config)
        elif isinstance(self.configs, RiceConfig):
            self.configs = [self.configs, config]
