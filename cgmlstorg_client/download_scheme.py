# Copyright 2024, Peter van Heusden <pvanheusden@uwc.ac.za>
#
# This source code is licensed under the MIT License
# found in the LICENSE file in the root directory of this source tree.

import sys

from pathlib import Path
from io import StringIO

import httpx

from Bio import SeqIO
from tqdm import tqdm

from .utils import get


def download_scheme(
    base_url: str,
    scheme_name: str,
    output_dir: Path,
    continue_partial_download: bool = False,
) -> int:
    client = httpx.Client()
    try:
        base_response = get(base_url, client=client)
        scheme = None
        for scheme in base_response:
            if scheme["Scheme"] == scheme_name:
                break
        else:
            raise sys.exit(f"Scheme {scheme_name} not found in {base_url}")
        scheme_def = get(scheme["Scheme Href"], client=client)
        locus_count = int(scheme_def["Locus Count"])
        locus_list = get(scheme_def["Locus Href"], client=client)
        assert (
            len(locus_list) == locus_count
        ), f"Locus count {locus_count} does not match locus list length {len(locus_list)} for {scheme_name}"

        output_dir.mkdir(parents=True, exist_ok=True)

        for locus_info in tqdm(locus_list, desc="Downloading alleles", unit="locus"):
            locus_name = locus_info["Locus"]
            locus_detail_lookup = {}

            locus_output_filename = output_dir / (locus_name + ".fasta")
            existing_size = (
                locus_output_filename.stat().st_size
                if locus_output_filename.exists()
                else 0
            )
            if continue_partial_download:
                headers = get(
                    locus_info["Alleles Href"], client=client, headers_only=True
                )
                expected_size = int(headers["Content-Length"])
                if existing_size == expected_size:
                    continue

            for locus_detail in get(locus_info["Locus Href"], client=client):
                locus_detail_lookup[locus_detail["Allele Nr."]] = int(
                    locus_detail["Sequence Length"].replace(",", "")
                )

            allele_sequences = get(
                locus_info["Alleles Href"], client=client, plaintext=True
            )
            for seq_record in SeqIO.parse(StringIO(allele_sequences), "fasta"):
                assert (
                    len(seq_record.seq) == locus_detail_lookup[seq_record.id]
                ), f"Sequence length mismatch for allele {seq_record.id}"

            with open(locus_output_filename, "w") as locus_output_file:
                locus_output_file.write(allele_sequences)
    finally:
        client.close()

    return locus_count
