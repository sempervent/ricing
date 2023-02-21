#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Describe a *Config objects."""
from os import getenv
from io import BytesIO, StringIO
from uuid import uuid4, UUID
from datetime import datetime
from pathlib import Path
from shlex import split as shlsplit
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

    def load_file(self, contents=Union[str, bytes, StringIO, BytesIO]):
        """Load contents into path."""
        if isinstance(contents, str):
            self.path.write_text(data=contents, encoding=self.encoding)
        elif isinstance(contents, StringIO):
            self.path.write_text(contents.getvalue(), encoding=self.encoding)
        elif isinstance(contents, bytes):
            self.path.write_bytes(contents)
        elif isinstance(contents, BytesIO):
            self.path.write_bytes(contents._getvalue())


class Program(PathNameUUID):
    """Configure a Program for a rice by associating it with a config file."""
    executable: str
    config_path: Union[Path, str]

    @validator('config_path')
    def _config_path_validator(cls, config_path: Union[Path, str]) -> Path:
        """Convert a config path to a Path."""
        return convert_str_to_path(path=config_path)

    def call(self, *args) -> str:
        """Call the executable with args."""
        args = " ".join(map(str, args))
        return capture_cmd(shlsplit(self.executable + " " + args))


class File(PathNameUUID):
    """Configure a File for a rice."""
    program: Program


class RiceConfig(BaseModel):
    """Configure a rice."""
    id: UUID = uuid4()
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

    def add_prgoram(
        self, program: Program | None = None,
        programs: List[Program] | None = None,
    ):
        """Add a program to the programs attribute."""
        if isinstance(program, Program):
            if self.programs is None:
                self.programs = [program]
            elif isinstance(self.programs, list):
                self.programs.append(program)
            elif isinstance(self.programs, Program):
                self.programs = [self.programs, program]
        if all([isinstance(p, Program) for p in programs]):
            if self.programs is None:
                self.programs = programs
            elif isinstance(self.programs, list):
                self.programs.extend(programs)
            elif isinstance(self.programs, Program):
                self.programs = [self.programs] + programs


class Config(BaseModel):
    """A BaseConfig object."""
    created_at: datetime = datetime.now()  # create the config now
    system_user: str = capture_cmd('whoami')  # whoami?
    home: Path = RICE_HOME  # the directory where rice homing belongs
    db: RiceDB = RiceDB()
    # below are set by internal methods, but can be set on initialization
    configs: Optional[List[RiceConfig]] = None

    def add_config(
        self,
        config: RiceConfig | None = None,
        configs: List[RiceConfig] | None = None,
    ):
        """Add a RiceConfig to the system configuration."""
        if config is not None:
            if not isinstance(config, RiceConfig):
                raise TypeError(f'{config} object is not of type RiceConfig')
            if self.configs is None:
                self.configs = [config]
            elif isinstance(self.configs, list):
                self.configs.append(config)
            elif isinstance(self.configs, RiceConfig):
                self.configs = [self.configs, config]
        if configs is not None:
            if not all([isinstance(c, RiceConfig) for c in configs]):
                raise TypeError(
                    f'{configs} contains an object that is not a RiceConfig')
            if self.configs is None:
                self.configs = configs
            elif isinstance(self.configs, list):
                self.configs.extend(configs)
            elif isinstance(self.configs, RiceConfig):
                self.configs = [self.configs] + configs

    def retrieve_all_files(self, include_content: bool = False):
        """Retrieve the paths of all config files."""
        data = {}
        for config in self.configs:
            data[config] = {}
            for file in config.files:
                data[config]['files'].append(str(file.path))
                if include_content is True:
                    data[config]['content'].append(file.contents())
            for program in config.programs:
                data[config][program].append(program.name)
