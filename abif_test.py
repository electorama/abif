#!/usr/bin/python
import abif

# count the ballots in each of the test files:
def test_count_test001():
    obj = abif.ABIF('testfiles/test001.abif')
    assert obj.count() == 24

def test_count_test002():
    obj = abif.ABIF('testfiles/test002.abif')
    assert obj.count() == 24

def test_count_test003():
    obj = abif.ABIF('testfiles/test003.abif')
    assert obj.count() == 24

def test_count_test004():
    obj = abif.ABIF('testfiles/test004.abif')
    assert obj.count() == 100

def test_count_test005():
    obj = abif.ABIF('testfiles/test005.abif')
    assert obj.count() == 100

def test_count_test006():
    obj = abif.ABIF('testfiles/test006.abif')
    assert obj.count() == 100

def test_count_test007():
    obj = abif.ABIF('testfiles/test007.abif')
    assert obj.count() == 100

def test_count_test008():
    obj = abif.ABIF('testfiles/test008.abif')
    assert obj.count() == 100

def test_count_test009():
    obj = abif.ABIF('testfiles/test009.abif')
    assert obj.count() == 100

def test_count_test010():
    obj = abif.ABIF('testfiles/test010.abif')
    assert obj.count() == 100

def test_count_test011():
    obj = abif.ABIF('testfiles/test011.abif')
    assert obj.count() == 100

def test_count_test012():
    obj = abif.ABIF('testfiles/test012.abif')
    assert obj.count() == 100

def test_count_test013():
    obj = abif.ABIF('testfiles/test013.abif')
    assert obj.count() == 100

def test_count_test014():
    obj = abif.ABIF('testfiles/test014.abif')
    assert obj.count() == 100



