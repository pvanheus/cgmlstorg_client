#!/usr/bin/env python3

import click

from .config import __version__
from .list_schemes import list_schemes

@click.group()
@click.version_option(__version__)
def cli():
    pass

@click.command()
@click.option('--pattern', '-p', help='Regex pattern to filter scheme names')
@click.option('--names-only/--no-names-only', '-n', default=False, help='Only report names of schemes')
@click.option('--exclude-pattern', '-e', help='Regex pattern to filter scheme names')
@click.option('--base-url', '-b', help='Base URL for cgMLST.org API', default='https://cgmlst.org/ncs/api')
def list(pattern, names_only, exclude_pattern, base_url):
    """List cgMLST schemes from cgMLST.org API"""
    print(base_url)
    list_schemes(names_only, base_url, pattern, exclude_pattern)

cli.add_command(list)

