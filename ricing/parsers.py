#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Define argument parsers for the rice CLI tool."""
from argparse import ArgumentParser


def delete_parser():
    """Provide a parser for the delete function."""
    parser = ArgumentParser(
        prog="rice delete",
        description="delete a config (if specified) or clear the database "
        "with a backup if specified",
        epilog="Deleting is forever. Use with caution or specify --backup",
        add_help=True,
        allow_abbrev=True,
        exit_on_error=True,
    )
    parser.add_argument('--backup', action='store_true', type=bool,
                        default=False, dest='backup',
                        help="Backup the database before deletion.")
    return parser


def rice_parser():
    """The main argument parser."""
    parser = ArgumentParser(
        prog='rice',
        description='customize and version your rices')
    parser.add_subparsers(dest='command')
    parser.add_argument('-v', '--verbose', action="store_true', type=bool,
                        dest='verbose',
                        default=False, help="Make rice chatty.")
    return parser

