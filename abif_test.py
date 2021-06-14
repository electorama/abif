#!/usr/bin/python
import abif

# count the ballots in each of the test files:
def test_count_test001():
    obj = abif.ABIF('test001.abif')
    assert obj.count() == 24

def test_count_test002():
    obj = abif.ABIF('test002.abif')
    assert obj.count() == 24

def test_count_test003():
    obj = abif.ABIF('test003.abif')
    assert obj.count() == 24

def test_count_test004():
    obj = abif.ABIF('test004.abif')
    assert obj.count() == 100

def test_count_test005():
    obj = abif.ABIF('test005.abif')
    assert obj.count() == 100

def test_count_test006():
    obj = abif.ABIF('test006.abif')
    assert obj.count() == 100

def test_count_test007():
    obj = abif.ABIF('test007.abif')
    assert obj.count() == 100

def test_count_test008():
    obj = abif.ABIF('test008.abif')
    assert obj.count() == 100

def test_count_test009():
    obj = abif.ABIF('test009.abif')
    assert obj.count() == 100


