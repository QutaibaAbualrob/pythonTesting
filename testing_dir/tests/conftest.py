
import pytest
from models.account import Account


@pytest.fixture
def acc():
    return Account('Eter', '123456', 100)







