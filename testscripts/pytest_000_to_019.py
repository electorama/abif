#!/usr/bin/python
import lark
import os
import pytest
import sys

# Adding parent dir to PYTHONPATH:
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import abif

TEST_CASES = [
    {
        "id": "test000_empty",
        "file": None,  # No file, just testing parser initialization
        "description": "Testing whether ABIF parser loads"
    },
    {
        "id": "test001_isvalid",
        "file": "test001.abif",
        "valid": True,
        "count": 24,
        "min_linecount": 0,
        "max_linecount": 250,
        "description": "Unordered scores"
    },
    {
        "id": "test002_isvalid",
        "file": "test002.abif",
        "valid": True,
        "count": 24,
        "min_linecount": 0,
        "max_linecount": 165,
        "description": "Ranked ballots with ABCDEFGH candidate set"
    },
    {
        "id": "test003_isvalid",
        "file": "test003.abif",
        "valid": True,
        "count": 24,
        "min_linecount": 0,
        "max_linecount": 240,
        "description": "Scores using = and > as delimiters"
    },
    {
        "id": "test004_isvalid",
        "file": "test004.abif",
        "valid": True,
        "count": 100,
        "min_linecount": 0,
        "max_linecount": float('inf'),
        "description": "Bracketed inlined tokens and unordered scores"
    },
    {
        "id": "test005_notvalid",
        "file": "test005.abif",
        "valid": False,
        "error_starts_with": "No terminal defined",
        "description": "Declared, bracketed candidate tokens. Unordered scores. (NOT VALID)"
    },
    {
        "id": "test006_notvalid",
        "file": "test006.abif",
        "valid": False,
        "error_starts_with": "No terminal defined",
        "description": "Bracketed candidate tokens (declared). Ranked and scored. (NOT VALID)"
    },
    {
        "id": "test007_notvalid",
        "file": "test007.abif",
        "valid": False,
        "error_starts_with": "No terminal defined",
        "description": "Declared, bracketed candidate tokens. Ranked, no score. (NOT VALID)"
    },
    {
        "id": "test008_notvalid",
        "file": "test008.abif",
        "valid": False,
        "error_starts_with": "No terminal defined",
        "description": "Mixed bracketed candidate tokens (sans whitespace). (NOT VALID)"
    },
    {
        "id": "test009_notvalid",
        "file": "test009.abif",
        "valid": False,
        "error_starts_with": "No terminal defined",
        "description": "Asterisk-delimited multiplier. (NOT VALID)"
    },
    {
        "id": "test010_isvalid",
        "file": "test010.abif",
        "valid": True,
        "count": 100,
        "min_linecount": 207,
        "max_linecount": 225,
        "description": "Declared, bracketed candidate tokens. Unordered scores."
    },
    {
        "id": "test011_isvalid",
        "file": "test011.abif",
        "valid": True,
        "count": 100,
        "min_linecount": 206,
        "max_linecount": 230,
        "description": "Bracketed candidate tokens (declared). Ranked and scored."
    },
    {
        "id": "test012_isvalid",
        "file": "test012.abif",
        "valid": True,
        "count": 100,
        "min_linecount": 156,
        "max_linecount": 168,
        "description": "Declared, bracketed candidate tokens. Ranked, no score."
    },
    {
        "id": "test013_isvalid",
        "file": "test013.abif",
        "valid": True,
        "count": 100,
        "min_linecount": 170,
        "max_linecount": 180,
        "description": "Mixed bracketed candidate tokens (sans whitespace)"
    },
    {
        "id": "test014_notvalid",
        "file": "test014.abif",
        "valid": False,
        "count": 100,
        "min_linecount": 210,
        "max_linecount": 235,
        "description": "Asterisk-delimited multiplier"
    },
    {
        "id": "test015_isvalid",
        "file": "test015.abif",
        "valid": True,
        "count": 100,
        "min_linecount": 200,
        "max_linecount": 220,
        "description": "Declared, bracketed candidate tokens. Unordered scores."
    },
    {
        "id": "test016_isvalid",
        "file": "test016.abif",
        "valid": True,
        "count": 100,
        "min_linecount": 205,
        "max_linecount": 225,
        "description": "Quoted candidate tokens (declared). Ranked and scored."
    },
    {
        "id": "test017_isvalid",
        "file": "test017.abif",
        "valid": True,
        "count": 100,
        "min_linecount": 215,
        "max_linecount": 235,
        "description": "Mix of quotes and brackets, with hash-but-not-comment"
    },
    {
        "id": "test018_isvalid",
        "file": "test018.abif",
        "valid": True,
        "count": 222230,
        "min_linecount": 290,
        "max_linecount": 320,
        "description": "RCV/IRV tiebreaker butterfly effect"
    },
    {
        "id": "test019_isvalid",
        "file": "test019.abif",
        "valid": True,
        "count": 100,
        "min_linecount": 210,
        "max_linecount": 235,
        "description": "Allowing for digits in cand_id (just not at the start)"
    }
]


@pytest.mark.parametrize("test_case", TEST_CASES, ids=[t["id"] for t in TEST_CASES])
def test_abif_file(test_case, request):
    """Test an ABIF file."""
    lark_parser = abif.ABIF_Parser()
    assert lark_parser != None

    # If there's no file given, just assume this is an initialization test
    if test_case["file"] == None:
        return

    # Pass ABIF testfile into Lark-based parser
    testfile = test_case["file"]
    larkobj = abif.ABIF_File(f"testfiles/{testfile}")

    # Check ballot count
    if "count" in test_case:
        try:
            larkobj.count()  == test_case["count"]
        except lark.exceptions.UnexpectedCharacters as e:
            if not test_case.get('valid'):
                pytest.xfail(f"{test_case['file']}: invalid ABIF - {e}")
            else:
                raise

    # Pull parsed ABIF string into a buffer
    try:
        abif_string = larkobj.parse()
    except lark.exceptions.UnexpectedCharacters as e:
        if not test_case.get('valid'):
            pytest.xfail(f"{test_case['file']}: invalid ABIF - {e}")
        else:
            raise

    # Check linecount against min_linecount and max_linecount
    linecount = abif_string.count('\n')
    if "min_linecount" in test_case:
        assert linecount >= test_case["min_linecount"]
    if "max_linecount" in test_case and test_case["max_linecount"] < float('inf'):
        assert linecount <= test_case["max_linecount"]
    
    # Check for Lark errors
    err = larkobj._get_error_string()
    if test_case.get("valid", True):
        assert err == None
    elif "error_starts_with" in test_case:
        assert err and err.startswith(test_case["error_starts_with"])
    
    # Try to transform and print results
    parseobj = larkobj.transform()
    if parseobj and hasattr(parseobj, "children"):
        print(f"TEST {test_case['id']} transform result:")
        for i, line in enumerate(parseobj.children[:5]):
            print(f"LINE {i}: {line}")
        if len(parseobj.children) > 5:
            print(f"... ({len(parseobj.children) - 5} more lines)")
    if not test_case.get('valid'):
        assert False, f"Test {test_case['id']} was expected to fail (valid=False) but passed"
