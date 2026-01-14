
def validate_phone(phone):
    return phone.isdigit() and len(phone) == 10

def test_valid_phone():
    assert validate_phone("0591234567")

def test_invalid_phone_letters():
    assert not validate_phone("05912abc67")

def test_invalid_phone_length():
    assert not validate_phone("059123")
