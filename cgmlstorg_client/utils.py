# Copyright 2024, Peter van Heusden <pvanheusden@uwc.ac.za>
#
# This source code is licensed under the MIT License
# found in the LICENSE file in the root directory of this source tree.

from typing import Any

import httpx


def get(
    url: str,
    plaintext: bool = False,
    headers_only: bool = False,
    client: httpx.Client | None = None,
) -> Any:

    if client is None:
        client = httpx.Client()
        internal_client = True
    else:
        internal_client = False

    try:
        if headers_only:
            response = client.head(url)
        else:
            response = client.get(url)
    finally:
        if internal_client:
            client.close()

    if response.status_code != 200:
        raise RuntimeError(
            f"Failed to fetch schemes from {url}, {response.status_code}: {response.text}"
        )

    if headers_only:
        return response.headers
    elif plaintext:
        return response.text
    else:
        return response.json()
