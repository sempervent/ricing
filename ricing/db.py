#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Provide a RiceDB class for interacting with the RICE_DB."""
from typing import Optional, Any
from sqlite3 import connect as connect2sqlite3

from pydantic import BaseModel

from ricing import RICE_CONFIG_DB

DB_CONNECTS = {
    'sqlite': connect2sqlite3
}


class RiceDB(BaseModel):
    """RiceDB connects to ricing's sqlite database."""
    conn_str: str = RICE_CONFIG_DB
    conn_fxn: str = 'sqlite'
    conn_kwargs: Optional[dict] = None  # TODO create models of specifics
    connection: Optional[Any] = None

    def __enter__(self):
        """Use with to enter database conneciton."""
        self.connect()
        return self

    def __exit__(self, _type, _value, _traceback):
        """Safely exit the connection."""
        self.close()

    def close(self):
        """Define a close method to end long running connection settings."""
        if hasattr(self.connection, 'close'):
            self.connection.close()
        self.connection = None

    def connect(self):
        """Safely connect to the database or keep a connection open."""
        if self.conn_kwargs is None:
            self.conn_kwargs = {}
        if self.connection is None:
            self.connection = DB_CONNECTS[self.conn_fxn](
                self.conn_str, **self.conn_kwargs)

    def open(self):
        """Open method to maintain a connection for long sessions."""
        self.connect()
