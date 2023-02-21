#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Provide an example database."""
from ricing.fxns import load_pkg_data, which_output
from ricing.config import Program, File, RiceConfig, Config


neofetch_prgrm = Program(
    name='neofetch',
    executable='neofetch',
    config_path='~/.config/neofetch',
    path=which_output('neofetch'),
)

neofetch_config = File(
    name='neofetch config',
    path='~/.config/neofetch/config.conf',
    program=neofetch_prgrm,
)


if __name__ == "__main__":
    print(neofetch_prgrm)
    print(neofetch_config)
