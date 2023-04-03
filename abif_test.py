#!/usr/bin/python
import abif
import lark

#========================================
# counting tests
# -------------------------------------

# The following tests count the ballots in each of the test files,
# using simple regexp-based parsing.  The files:
#
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

def test_larkparser_test000():
    lark_parser = abif.ABIF_Parser()
    print(lark_parser)
    assert lark_parser != None


def test_larkparser_test001():
    obj = abif.ABIF_File('testfiles/test001.abif')
    assert obj.count() == 24
    abif_string = obj.parse()

    assert abif_string != None
    linecount = abif_string.count('\n')
    assert linecount == 231
    err = obj._get_error_string()
    parseobj = obj.transform()

    for line in parseobj.children:
        print("LINE: ", line)
    assert err == None


def test_larkparser_test002():
    import lark
    obj = abif.ABIF_File('testfiles/test002.abif')
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
    assert linecount == 146
    err = obj._get_error_string()
    assert err == None


def test_larkparser_test003():
    obj = abif.ABIF_File('testfiles/test003.abif')
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
    assert linecount == 218
    err = obj._get_error_string()
    assert err == None


def test_b_larkparser_test004():
    obj = abif.ABIF_File('testfiles/test004.abif') 
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
    obj = abif.ABIF_File('testfiles/test005.abif')
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
    obj = abif.ABIF_File('testfiles/test006.abif')
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
    obj = abif.ABIF_File('testfiles/test007.abif')
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
    obj = abif.ABIF_File('testfiles/test008.abif')
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
    obj = abif.ABIF_File('testfiles/test009.abif')
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
# Test cases 010 through 014
#
# This are replacement test cases for 005 through 009.  ABIF issue #8
# (<https://github.com/electorama/abif/issues/8>) describes the change
# in syntax.


def test_larkparser_test010():
    obj = abif.ABIF_File('testfiles/test010.abif')
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
    assert linecount < 215
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
    assert linecount < 216
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
    assert linecount > 170
    assert linecount < 180
    err = obj._get_error_string()
    assert err == None


def test_larkparser_test014():
    obj = abif.ABIF_File('testfiles/test014.abif')
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
    assert linecount > 210
    assert linecount < 230
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
    assert linecount < 210
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
    assert linecount < 220
    err = obj._get_error_string()
    assert err == None



