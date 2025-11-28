# Copyright 2025 Xin Huang
#
# GNU General Public License v3.0
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, please see
#
#    https://www.gnu.org/licenses/gpl-3.0.en.html


import pytest
import yaml
from sai.utils import UniqueKeyLoader


def test_unique_key_loader_single_mapping_no_duplicates():
    yaml_str = """
    fd: True
    df: False
    """
    data = yaml.load(yaml_str, Loader=UniqueKeyLoader)

    assert isinstance(data, dict)
    assert data["fd"] is True
    assert data["df"] == False


def test_unique_key_loader_nested_mapping_no_duplicates():
    yaml_str = """
    statistics:
      Danc: False
      Dplus: True
    ploidies:
      ref:
        REF: 2
      tgt:
        TGT: 4
      src:
        SRC: 4
    """
    data = yaml.load(yaml_str, Loader=UniqueKeyLoader)

    assert isinstance(data, dict)
    assert data["statistics"]["Danc"] is False
    assert data["statistics"]["Dplus"] is True
    assert data["ploidies"]["ref"]["REF"] == 2
    assert data["ploidies"]["tgt"]["TGT"] == 4
    assert data["ploidies"]["src"]["SRC"] == 4


def test_unique_key_loader_raises_on_duplicate_top_level_key():
    yaml_str = """
    DD: False
    DD: True
    """
    with pytest.raises(ValueError) as excinfo:
        yaml.load(yaml_str, Loader=UniqueKeyLoader)

    msg = str(excinfo.value)
    assert "Duplicate key in YAML" in msg
    assert "'DD'" in msg


def test_unique_key_loader_raises_on_duplicate_nested_key():
    yaml_str = """
    statistics:
      fd: False
      fd: True
      df: True
    """
    with pytest.raises(ValueError) as excinfo:
        yaml.load(yaml_str, Loader=UniqueKeyLoader)

    msg = str(excinfo.value)
    assert "Duplicate key in YAML" in msg
    assert "'fd'" in msg
