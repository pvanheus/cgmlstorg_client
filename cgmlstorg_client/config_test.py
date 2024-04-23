# Copyright 2024, Peter van Heusden <pvanheusden@uwc.ac.za>
#
# This source code is licensed under the MIT License
# found in the LICENSE file in the root directory of this source tree.

import glob
import io
import subprocess

import cgmlstorg_client


def test_version() -> None:
    assert cgmlstorg_client.__version__


def test_copyright() -> None:
    """Check that source code files contain a copyright line"""
    for fname in glob.glob("cgmlstorg_client/**/*.py", recursive=True):
        print("Checking " + fname + " for copyright header")

        with open(fname) as f:
            for line in f.readlines():
                if not line.strip():
                    continue
                assert line.startswith("# Copyright")
                break


def test_about() -> None:
    out = io.StringIO()
    cgmlstorg_client.about(out)
    print(out)


def test_about_main() -> None:
    rval = subprocess.call(["python", "-m", "cgmlstorg_client.about"])
    assert rval == 0

if __name__ == '__main__':
    test_copyright()