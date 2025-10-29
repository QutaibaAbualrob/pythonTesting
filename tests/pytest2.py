


import pytest
import models.functions as func


def test_add():
    result = func.add(4, 5)
    assert result == 10