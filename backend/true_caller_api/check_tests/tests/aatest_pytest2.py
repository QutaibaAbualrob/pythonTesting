


import pytest
import models.functions as func


def test_add():
    result = func.add(4, 5)
    assert result == 9
    
def test_divide():
    result = func.divide(10, 5)
    assert result == 2

def test_divide_byzero():
    # To check if a functions behaves as required, here
    # its expected for the function to raise as ValueError as implemented
    # in divide function
    #
    # this would show up if it didnt pass
    # FAILED tests/pytest2.py::test_divide_byzero - Failed: DID NOT RAISE <class 'ValueError'>
    #
    with pytest.raises(ValueError):
        func.divide(10, 1)
        
def test_string_addition():
    result = func.add('this is test for', ' strings')
    assert result == 'this is test for strings'