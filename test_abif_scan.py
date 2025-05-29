#!/usr/bin/env python3
"""
test_abif_scan.py - Scans for .abif files and runs basic tests on them.

This test discovers all .abif files in the project directory structure
and runs a basic validation test against each file.
"""

import abif
import os
import pathlib
import pytest
import sys
import typing

EXTRA_ABIF_DIR="extra_abif"

def find_all_abif_files(abif_dir_to_scan) -> typing.List[pathlib.Path]:
    """Find all .abif files in all subdirectories."""
    root_dir = pathlib.Path(abif_dir_to_scan)
    abif_files = list(root_dir.glob("**/*.abif"))
    return sorted(abif_files)


@pytest.mark.parametrize("abif_file", find_all_abif_files(EXTRA_ABIF_DIR))
def test_is_abif_valid(abif_file):
    """Test that each .abif file exists and can be read."""
    assert abif_file.exists(), f"ABIF file {abif_file} does not exist"
    jabmod = abif.convert_abif_file_to_jabmod(abif_file)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        files = find_all_abif_files(sys.argv[1])
    else:
        files = find_all_abif_files(EXTRA_ABIF_DIR)
    print(f"Found {len(files)} ABIF files:")
    for file in files:
        print(f"  {file}")
        jabmod = abif.convert_abif_file_to_jabmod(file)
