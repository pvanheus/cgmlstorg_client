# Copyright 2024, Peter van Heusden <pvanheusden@uwc.ac.za>
#
# This source code is licensed under the MIT License
# found in the LICENSE file in the root directory of this source tree.

import re

import click
import httpx

from tqdm import tqdm

from .utils import get


def get_cgmlst_schemes(
    base_url: str,
    pattern: str | None = None,
    exclude_pattern: str | None = None,
    names_only: bool = False,
) -> list[dict]:

    client = httpx.Client()
    try:
        base_response = get(base_url, client=client)

        scheme_list: list[dict[str, str]] = []
        for index, scheme in tqdm(
            enumerate(base_response),
            desc="Fetching schemes",
            unit="scheme",
            total=len(base_response),
        ):
            if exclude_pattern is not None:
                if re.search(exclude_pattern, scheme["Scheme"], re.IGNORECASE):
                    continue
            if pattern is not None:
                scheme_match = re.search(pattern, scheme["Scheme"])
                include_scheme = scheme_match is not None
            else:
                include_scheme = True
            if include_scheme:
                scheme_details = {}
                scheme_name = scheme["Scheme"]
                scheme_details["name"] = scheme_name
                if not names_only:
                    # name    id      description     locus_count     records last_added      last_updated
                    scheme_details["id"] = index
                    scheme_details["locus_count"] = scheme["Target Count"]
                    scheme_details["records"] = "UNKNOWN"
                    scheme_def = get(scheme["Scheme Href"], client=client)
                    last_updated_match = re.search(
                        r"\([^;]+, (\d+-\w+-\d+).*\)", scheme_def["Seed Genome"]
                    )
                    if last_updated_match:
                        scheme_details["last_added"] = last_updated_match.group(1)
                    else:
                        scheme_details["last_added"] = "UNKNOWN"
                    scheme_details["last_updated"] = scheme_def.get(
                        "Last Change", "UNKNOWN"
                    )
                scheme_list.append(dict(scheme_details))
    finally:
        client.close()

    return scheme_list


fields = ["name", "id", "locus_count", "records", "last_added", "last_updated"]


def list_schemes(
    names_only: bool = False,
    base_url: str = "https://cgmlst.org/ncs/api",
    pattern: str | None = None,
    exclude_pattern: str | None = None,
) -> None:

    schemes = get_cgmlst_schemes(base_url, pattern, exclude_pattern, names_only)

    if names_only:
        click.echo("name")
    else:
        click.echo("\t".join(fields))

    for entry in schemes:
        if names_only:
            click.echo(entry["name"])
        else:
            click.echo("\t".join(str(entry[field]) for field in fields))
