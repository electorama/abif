#!/usr/bin/python
import lark
import os
import pytest
import sys

# Adding parent dir to PYTHONPATH:
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import abif

#========================================
# counting tests
# -------------------------------------

# The following tests count the ballots in each of the test files,
# using simple regexp-based parsing.  The files:
#
# test000 (no file) - testing whether abif loads
# test001.abif - unordered scores
# test002.abif - ranked ballots with ABCDEFGH candidate set
# test003.abif - Scores using = and > as delimiters
# test004.abif - bracketed inlined tokens and unordered scores
# test005.abif - Declared, bracketed candidate tokens.  Unordered scores.
# test006.abif - Bracketed candidate tokens (declared).  Ranked and scored.
# test007.abif - Declared, bracketed candidate tokens. Ranked, no score.
# test008.abif - Mixed bracketed candidate tokens (sans whitespace)
# test009.abif - Asterisk-delimited multiplier
# test010.abif - Declared, bracketed candidate tokens.  Unordered scores.
# test011.abif - Bracketed candidate tokens (declared).  Ranked and scored.
# test012.abif - Declared, bracketed candidate tokens. Ranked, no score.
# test013.abif - Mixed bracketed candidate tokens (sans whitespace)
# test014.abif - Asterisk-delimited multiplier
# test015.abif - Declared, bracketed candidate tokens.  Unordered scores.
# test016.abif - Quoted candidate tokens (declared).  Ranked and scored.
# test017.abif - Mix of quotes and brackets, with hash-but-not-comment
# test018.abif - RCV/IRV tiebreaker butterfly effect
# test019.abif - Allowing for digits in cand_id (just not at the start)

def test_larkparser_test000():
    lark_parser = abif.ABIF_Parser()
    print(lark_parser)
    assert lark_parser != None


def test_larkparser_test001():
    testfile = 'test001.abif'
    obj = abif.ABIF_File(f"testfiles/{testfile}")
    assert obj.count() == 24
    abif_string = obj.parse()

    assert abif_string != None
    linecount = abif_string.count('\n')
    assert linecount < 250
    err = obj._get_error_string()
    parseobj = obj.transform()

    for line in parseobj.children:
        print("LINE: ", line)
    assert err == None

def test_larkparser_test002():
    testfile = 'test002.abif'
    obj = abif.ABIF_File(f"testfiles/{testfile}")
    assert obj.count() == 24
    abif_string = ""
    try:
        abif_string = obj.parse()
    except lark.exceptions.UnexpectedCharacters as err:
        print(str(err))
        pass
    except:
        pass
    assert abif_string != None
    linecount = abif_string.count('\n')
    assert linecount < 165
    err = obj._get_error_string()
    assert err == None


def test_larkparser_test003():
    testfile = 'test003.abif'
    obj = abif.ABIF_File(f"testfiles/{testfile}")
    assert obj.count() == 24
    abif_string = ""
    try:
        abif_string = obj.parse()
    except lark.exceptions.UnexpectedCharacters as err:
        print(str(err))
        pass
    except:
        pass
    assert abif_string != None
    linecount = abif_string.count('\n')
    assert linecount < 240
    err = obj._get_error_string()
    assert err == None


def test_b_larkparser_test004():
    testfile = 'test004.abif'
    obj = abif.ABIF_File(f"testfiles/{testfile}")
    assert obj.count() == 100
    abif_string = ""
    try:
        abif_string = obj.parse()
    except lark.exceptions.UnexpectedCharacters as err:
        print(str(err))
        pass
    except:
        pass
    assert abif_string != None
    print("TEST 004 abif_string len: ", len(abif_string))
    linecount = abif_string.count('\n')
    err = obj._get_error_string()
    assert err == None


#############################################################
# THROWING EXCEPTIONS ON PURPOSE
#
# test005.abif through test009.abif should raise assertions, because
# they were written before we agreed that candidate id declaration
# lines should start with "=", then the id, and *then* the "squoted"
# (square-braket quoted) UTF-8 version of their name with spaces and
# accent marks and tildes in it.

def test_larkparser_test005():
    testfile = 'test005.abif'
    pytest.xfail(f"{testfile}: invalid ABIF")
    obj = abif.ABIF_File(f"testfiles/{testfile}")
    try:
        abif_string = obj.parse()
    except lark.exceptions.UnexpectedCharacters as err:
        abif_string = "FAIL"
        print(str(err))
        pass
    except:
        pass
    assert abif_string != None
    linecount = abif_string.count('\n')
    assert linecount == 0
    err = obj._get_error_string()
    assert err.startswith('No terminal defined')


def test_larkparser_test006():
    testfile = 'test006.abif'
    pytest.xfail(f"{testfile}: invalid ABIF")
    obj = abif.ABIF_File(f"testfiles/{testfile}")
    try:
        abif_string = obj.parse()
    except lark.exceptions.UnexpectedCharacters as err:
        abif_string = "FAIL"
        print(str(err))
        pass
    except:
        pass
    assert abif_string != None
    linecount = abif_string.count('\n')
    assert linecount == 0
    err = obj._get_error_string()
    assert err.startswith('No terminal defined')


def test_larkparser_test007():
    testfile = 'test007.abif'
    pytest.xfail(f"{testfile}: invalid ABIF")
    obj = abif.ABIF_File(f"testfiles/{testfile}")
    try:
        abif_string = obj.parse()
    except lark.exceptions.UnexpectedCharacters as err:
        abif_string = "FAIL"
        print(str(err))
        pass
    except:
        pass
    assert abif_string != None
    linecount = abif_string.count('\n')
    assert linecount == 0
    err = obj._get_error_string()
    assert err.startswith('No terminal defined')


def test_b_larkparser_test008():
    testfile = 'test008.abif'
    pytest.xfail(f"{testfile}: invalid ABIF")
    obj = abif.ABIF_File(f"testfiles/{testfile}")
    try:
        abif_string = obj.parse()
    except lark.exceptions.UnexpectedCharacters as err:
        abif_string = "FAIL"
        print(str(err))
        pass
    except:
        pass
    assert abif_string != None
    linecount = abif_string.count('\n')
    assert linecount == 0
    err = obj._get_error_string()
    assert err.startswith('No terminal defined')


def test_b_larkparser_test009():
    testfile = 'test009.abif'
    pytest.xfail(f"{testfile}: invalid ABIF")
    obj = abif.ABIF_File(f"testfiles/{testfile}")
    try:
        abif_string = obj.parse()
    except lark.exceptions.UnexpectedCharacters as err:
        abif_string = "FAIL"
        print(str(err))
        pass
    except:
        pass
    assert abif_string != None
    linecount = abif_string.count('\n')
    assert linecount == 0
    err = obj._get_error_string()
    assert err.startswith('No terminal defined')


###########################################################
# Test cases 010 through 016
#
# This are replacement test cases for 005 through 009.  ABIF issue #8
# (<https://github.com/electorama/abif/issues/8>) describes the change
# in syntax.


def test_larkparser_test010():
    testfile = 'test010.abif'
    obj = abif.ABIF_File(f"testfiles/{testfile}")
    assert obj.count() == 100
    abif_string = ""
    try:
        abif_string = obj.parse()
    except lark.exceptions.UnexpectedCharacters as err:
        print(str(err))
        pass
    except:
        pass
    assert abif_string != None
    linecount = abif_string.count('\n')
    assert linecount > 207
    assert linecount < 225
    err = obj._get_error_string()
    assert err == None


def test_larkparser_test011():
    obj = abif.ABIF_File('testfiles/test011.abif')
    assert obj.count() == 100
    abif_string = ""
    try:
        abif_string = obj.parse()
    except lark.exceptions.UnexpectedCharacters as err:
        print(str(err))
        pass
    except:
        pass
    assert abif_string != None
    linecount = abif_string.count('\n')
    assert linecount > 206
    assert linecount < 230
    err = obj._get_error_string()
    assert err == None


def test_larkparser_test012():
    obj = abif.ABIF_File('testfiles/test012.abif')
    assert obj.count() == 100
    abif_string = ""
    try:
        abif_string = obj.parse()
    except lark.exceptions.UnexpectedCharacters as err:
        print(str(err))
        pass
    except:
        pass
    assert abif_string != None
    linecount = abif_string.count('\n')
    assert linecount < 168
    assert linecount > 156
    err = obj._get_error_string()
    assert err == None


def test_larkparser_test013():
    obj = abif.ABIF_File('testfiles/test013.abif')
    assert obj.count() == 100
    abif_string = ""
    try:
        abif_string = obj.parse()
    except lark.exceptions.UnexpectedCharacters as err:
        print(str(err))
        pass
    except:
        pass
    assert abif_string != None
    linecount = abif_string.count('\n')
    assert linecount >= 170
    assert linecount <= 180
    err = obj._get_error_string()
    assert err == None


def test_larkparser_test014():
    testfile = 'test014.abif'
    pytest.xfail(f"{testfile}: invalid ABIF")
    obj = abif.ABIF_File(f"testfiles/{testfile}")
    assert obj.count() == 100
    abif_string = ""
    try:
        abif_string = obj.parse()
    except lark.exceptions.UnexpectedCharacters as err:
        print(str(err))
        pass
    except:
        pass
    assert abif_string != None
    linecount = abif_string.count('\n')
    assert linecount >= 210
    assert linecount <= 235
    err = obj._get_error_string()
    assert err == None


def test_larkparser_test015():
    obj = abif.ABIF_File('testfiles/test015.abif')
    assert obj.count() == 100
    abif_string = ""
    try:
        abif_string = obj.parse()
    except lark.exceptions.UnexpectedCharacters as err:
        print(str(err))
        pass
    except:
        pass
    assert abif_string != None
    linecount = abif_string.count('\n')
    assert linecount > 200
    assert linecount < 220
    err = obj._get_error_string()
    assert err == None


def test_larkparser_test016():
    obj = abif.ABIF_File('testfiles/test016.abif')
    assert obj.count() == 100
    abif_string = ""
    try:
        abif_string = obj.parse()
    except lark.exceptions.UnexpectedCharacters as err:
        print(str(err))
        pass
    except:
        pass
    assert abif_string != None
    linecount = abif_string.count('\n')
    assert linecount > 205
    assert linecount < 225
    err = obj._get_error_string()
    assert err == None


def test_larkparser_test017():
    obj = abif.ABIF_File('testfiles/test017.abif')
    assert obj.count() == 100
    abif_string = ""
    try:
        abif_string = obj.parse()
    except lark.exceptions.UnexpectedCharacters as err:
        print(str(err))
        pass
    except:
        pass
    assert abif_string != None
    linecount = abif_string.count('\n')
    assert linecount > 215
    assert linecount < 235
    err = obj._get_error_string()
    assert err == None


def test_larkparser_test018():
    obj = abif.ABIF_File('testfiles/test018.abif')
    assert obj.count() == 222230
    abif_string = ""
    try:
        abif_string = obj.parse()
    except lark.exceptions.UnexpectedCharacters as err:
        print(str(err))
        pass
    except:
        pass
    assert abif_string != None
    linecount = abif_string.count('\n')
    assert linecount > 290
    assert linecount < 320
    err = obj._get_error_string()
    assert err == None

# test019.abif - Allowing for digits in cand_id (just not at the start)
def test_larkparser_test019():
    obj = abif.ABIF_File('testfiles/test019.abif')
    assert obj.count() == 100
    abif_string = ""
    try:
        abif_string = obj.parse()
    except lark.exceptions.UnexpectedCharacters as err:
        print(str(err))
        pass
    except:
        pass
    assert abif_string != None
    linecount = abif_string.count('\n')
    assert linecount >= 210
    assert linecount <= 235
    err = obj._get_error_string()
    assert err == None


