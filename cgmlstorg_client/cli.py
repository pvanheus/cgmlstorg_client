# Copyright 2024, Peter van Heusden <pvanheusden@uwc.ac.za>
#
# This source code is licensed under the MIT License
# found in the LICENSE file in the root directory of this source tree.

from pathlib import Path
from typing import Any

import click

from .config import __version__
from .list_schemes import list_schemes
from .download_scheme import download_scheme


class CgmlstorgCli(click.Command):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.params.insert(
            0,
            click.Option(
                ["--base-url", "-b"],
                help="Base URL for cgMLST.org API",
                default="https://cgmlst.org/ncs/api",
            ),
        )


@click.group()
@click.version_option(__version__)
def cli() -> None:
    pass


@click.command(cls=CgmlstorgCli)
@click.option("--pattern", "-p", help="Regex pattern to filter scheme names")
@click.option(
    "--names-only/--no-names-only",
    "-n",
    default=False,
    help="Only report names of schemes",
)
@click.option("--exclude-pattern", "-e", help="Regex pattern to filter scheme names")
def list(pattern: str, names_only: bool, exclude_pattern: str, base_url: str) -> None:
    """List cgMLST schemes from cgMLST.org API"""
    list_schemes(names_only, base_url, pattern, exclude_pattern)


cli.add_command(list)


@click.command(cls=CgmlstorgCli)
@click.option("--scheme-name", "-s", help="Name of scheme to download", required=True)
@click.option(
    "--output-dir",
    "-o",
    help="Output directory for scheme files",
    type=click.Path(),
    required=True,
)
@click.option(
    "--continue",
    "-c",
    "continue_partial",
    is_flag=True,
    help="Continue partial downloads from previous run",
)
def download(scheme_name: str, output_dir: Path, base_url: str, continue_partial: bool) -> None:
    """Download a cgMLST scheme from cgMLST.org API"""
    locus_count = download_scheme(
        base_url, scheme_name, Path(output_dir), continue_partial
    )
    click.echo(f"Downloaded {locus_count} loci for {scheme_name} to {output_dir}")


cli.add_command(download)
