#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Describe the ricing sql model."""
from uuid import uuid4

from sqlalchemy import (
    Column, Integer, String, Table, create_engine, ForeignKey
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from ricing import RICE_CONFIG_DB

Base = declarative_base()

# create many-to-many for Config <=> File
config_file_relations = Table(
    'config_file_relations',
    Base.metadata,
    Column('config_id', Integer, ForeignKey('config.id')),
    Column('file_id', String, ForeignKey('file.id')),
)

class Config(Base):
    __tablename__ = 'config'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    files = relationship('File', secondary=config_file_relations)
    programs = relationship('Program', back_populates='config')


class File(Base):
    __tablename__ = "file"
    id = Column(String, primary_key=True, default=str(uuid4()))
    hash = Column(String)
    contents = Column(String)
    path = Column(String)
    name = Column(String)
    programs = relationship('Program', back_populates='file')


class Program(Base):
    __tablename__ = "program"
    id = Column(String, primary_key=True, default=str(uuid4()))
    name = Column(String)
    path = Column(String)
    config_id = Column(Integer, ForeignKey('config.id'))
    config = relationship('Config', back_populates='program')
    file_id = Column(String, ForeignKey('file.id'))
    file = relationship('File', back_populates='program')


def create_rice_db(connection_str: str | None, **kwargs):
    """Create the rice database for storing configs.
    Args:
        connection_str: optional string for sqlalchemy to connect on
        kwargs: optional arguments to create_engine
    """
    if connection_str is None:
        connection_str = RICE_CONFIG_DB
    engine = create_engine(connection_str, **kwargs)
    Base.metadata.create_all(engine)

