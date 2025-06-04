#!/usr/bin/env python3
"""
test_abif_interop.py - Tests interoperability between abif.py and abiflib.

This script discovers .abif files and tests that the jabmod output from abif.py
can be successfully processed by abiflib.
"""

import abif
import json
import os
import pathlib
import pytest
import sys
import typing

# Import functions from abiflib
from abiflib import (
    convert_abif_to_jabmod,
    convert_jabmod_to_abif,
    ABIFVotelineException
)

EXTRA_ABIF_DIR = "extra_abif"

def find_all_abif_files(abif_dir_to_scan) -> typing.List[pathlib.Path]:
    """Find all .abif files in all subdirectories."""
    root_dir = pathlib.Path(abif_dir_to_scan)
    abif_files = list(root_dir.glob("**/*.abif"))
    return sorted(abif_files)


@pytest.mark.parametrize("abif_file", find_all_abif_files(EXTRA_ABIF_DIR))
def test_abif_interoperability(abif_file):
    """Test that jabmod from abif.py can be used by abiflib."""
    assert abif_file.exists(), f"ABIF file {abif_file} does not exist"
    
    # Step 1: Parse with abif.py
    abif_py_jabmod = abif.convert_abif_file_to_jabmod(abif_file)
    
    # Step 2: Verify key structure
    assert "candidates" in abif_py_jabmod, "Candidates missing in jabmod"
    assert "metadata" in abif_py_jabmod, "Metadata missing in jabmod"
    assert "votelines" in abif_py_jabmod, "Votelines missing in jabmod"
    assert "ballotcount" in abif_py_jabmod["metadata"], "Ballot count missing in metadata"
    
    # Step 3: Convert jabmod to ABIF using abiflib
    try:
        abif_output = convert_jabmod_to_abif(abif_py_jabmod)
        assert len(abif_output) > 0, "Empty ABIF output"
    except Exception as e:
        pytest.fail(f"convert_jabmod_to_abif failed: {e}")
    
    # Step 4: Round-trip test
    try:
        # Convert the ABIF back to jabmod using abiflib
        abiflib_jabmod = convert_abif_to_jabmod(abif_output)
        
        # Compare key structures
        assert len(abif_py_jabmod["votelines"]) == len(abiflib_jabmod["votelines"]), "Vote line count mismatch"
        assert abif_py_jabmod["metadata"]["ballotcount"] == abiflib_jabmod["metadata"]["ballotcount"], "Ballot count mismatch"
        assert sorted(abif_py_jabmod["candidates"].keys()) == sorted(abiflib_jabmod["candidates"].keys()), "Candidate keys mismatch"
    except ABIFVotelineException as e:
        pytest.fail(f"ABIFVotelineException: {e}")
    except Exception as e:
        pytest.fail(f"Round-trip conversion failed: {e}")


@pytest.mark.parametrize("abif_file", find_all_abif_files(EXTRA_ABIF_DIR))
def test_candidate_inference(abif_file):
    """Test that candidates are properly inferred from votelines."""
    jabmod = abif.convert_abif_file_to_jabmod(abif_file)
    
    # Find all candidates mentioned in votelines
    all_voteline_candidates = set()
    for voteline in jabmod["votelines"]:
        for candidate in voteline["prefs"].keys():
            all_voteline_candidates.add(candidate)
    
    # Every candidate used in votelines should be defined
    for candidate in all_voteline_candidates:
        assert candidate in jabmod["candidates"], f"Candidate {candidate} used in votelines but not defined in candidates section"


def cli_parse_summary(abif_file):
    """Command-line version forparsing /roundtripping single files without pytest."""
    print("============================")
    print(f"Parse results for {abif_file}")
    print("----------------")

    # Convert to jabmod using abif.py
    abif_py_jabmod = abif.convert_abif_file_to_jabmod(abif_file)
    print(f"Parsed {len(abif_py_jabmod['votelines'])} vote lines with {len(abif_py_jabmod['candidates'])} candidates")

    # Print candidates
    print("\nCandidates:")
    for cand_id, cand_name in abif_py_jabmod["candidates"].items():
        print(f"  {cand_id}: {cand_name}")

    # Convert to ABIF using abiflib
    abif_output = convert_jabmod_to_abif(abif_py_jabmod)
    print(f"\nConverted to ABIF: {len(abif_output)} characters")
    print(f"ABIF top portion:\n {abif_output[:400]}...")
        
    # Convert back to jabmod using abiflib
    abiflib_jabmod = convert_abif_to_jabmod(abif_output)

    print(f"Ballot count: {abiflib_jabmod['metadata']['ballotcount']}")

    print(f"{sorted(abif_py_jabmod['candidates'].keys())=}")
    print(f"{sorted(abiflib_jabmod['candidates'].keys())=}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        files = sys.argv[1:]
    else:
        files = find_all_abif_files(EXTRA_ABIF_DIR)

    for file in files:
        cli_parse_summary(file)
