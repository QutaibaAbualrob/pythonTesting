


import pytest
from models.account import Account 


def test_account_exists(acc):
    flag = False
    if acc:
        flag = True

    assert flag


def test_widthdraw_right_balance(acc):
    amount = 100
    result = acc.balance - amount
    assert result >= 0

def test_deposite_allowed_amount(acc):
    amount = 100
    assert (amount <= acc.allowed)

def test_valid_card_number(acc):
    assert len(acc.getCard()) >= 6