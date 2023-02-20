#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Provide a RiceDB class for interacting with the RICE_DB."""
from typing import Callable, Optional
from sqlite3 import connect as connect2sqlite3, Connection

from pydantic import BaseModel

from ricing import RICE_DB


class RiceDB(BaseModel):
    """This RiceDB connects to ricing's sqlite database."""
    conn_str: str = RICE_DB
    conn_fxn: Callable = connect2sqlite3
    conn_kwargs: Optional[dict] = None
    connection: Optional[Connection] = None

    def __enter__(self):
        """Use with to enter database conneciton."""
        if self.conn_kwargs is None:
            self.conn_kwargs = {}
        self.connection = self.conn_fxn(self.conn_str, **self.conn_kwargs)
        return self

    def __exit__(self, _type, _value, _traceback):
        """Safely exist the connection."""
        if hasattr(self.connection, 'close'):
            self.connection.close()
        self.connection = None

