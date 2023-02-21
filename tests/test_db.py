#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test the RiceDB class."""
from sqlite3 import Connection

from ricing.sql import RiceDB, DB_CONNECTS


def test_RiceDB():
    """Test the RiceDB class."""
    ricedb = RiceDB()
    testdb = RiceDB(conn_str=":memory:")
    dbs = [ricedb, testdb]
    for db in dbs:
        assert db.connection is None
        assert db.conn_fxn in DB_CONNECTS
