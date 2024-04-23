# Copyright 2024, Peter van Heusden <pvanheusden@uwc.ac.za>
#
# This source code is licensed under the MIT License
# found in the LICENSE file in the root directory of this source tree.

from .list_schemes import get_cgmlst_schemes, fields


base_url = "https://cgmlst.org/ncs/api"


def test_get_schemes() -> None:
    schemes = get_cgmlst_schemes("https://cgmlst.org/ncs/api")
    assert len(schemes) > 0
    for scheme in schemes:
        for field in fields:
            assert field in scheme


def test_get_schemes_names_only() -> None:
    schemes = get_cgmlst_schemes("https://cgmlst.org/ncs/api", names_only=True)
    assert len(schemes) > 0
    for scheme in schemes:
        assert "name" in scheme


def test_get_schemes_include() -> None:
    schemes = get_cgmlst_schemes("https://cgmlst.org/ncs/api", pattern='^Acinetobacter', names_only=True)
    assert len(schemes) > 0
    for scheme in schemes:
        assert "name" in scheme
        assert scheme["name"].startswith("Acinetobacter")


def test_get_schemes_exclude() -> None:
    schemes = get_cgmlst_schemes("https://cgmlst.org/ncs/api", exclude_pattern='^Acinetobacter', names_only=True)
    assert len(schemes) > 0
    for scheme in schemes:
        assert "name" in scheme
        assert not scheme["name"].startswith("Acinetobacter")
