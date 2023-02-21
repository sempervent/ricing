#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test the fxn implementations."""
from os import environ
from pathlib import Path

import pytest

from ricing.fxns import capture_cmd, which_output


@pytest.mark.parametrize(
    'cmd',
    ['whoami', 'ls', 'ls -lash', 'ls -lash | grep .py',])
def test_capture_cmd():
    """Test capture_cmd."""
    output = capture_cmd('whoami')
    assert isinstance(output, str)
    if cmd == 'whoami':
        assert output == environ['USER']


def test_which_output():
    """Test that the which output leads to an executable."""
    which_ls = which_output('ls')
    assert isinstance(which_ls, str)
