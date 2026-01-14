
def can_search(current_count, limit=5):
    return current_count < limit

def test_under_limit():
    assert can_search(3)

def test_equal_limit():
    assert not can_search(5)

def test_over_limit():
    assert not can_search(6)
