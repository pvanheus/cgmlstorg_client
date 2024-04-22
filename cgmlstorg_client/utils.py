#!/usr/bin/env python3

from typing import Any

import requests

from requests.adapters import HTTPAdapter, Retry


def get(url: str,
        max_retries: int = 5,
        session: requests.Session | None = None) -> Any:
    if session is None:
        session = requests.Session()

    retries = Retry(total=max_retries,
                    backoff_factor=0.1,
                    status_forcelist=[ 500, 502, 503, 504 ])
    
    session.mount('https://', HTTPAdapter(max_retries=retries))

    response = session.get(url)
    if response.status_code != 200:
        raise RuntimeError(f"Failed to fetch schemes from {url}, {response.status_code}: {response.text}")

    return response.json()