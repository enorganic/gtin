from decimal import Decimal
from gtin import GTIN

def test_check_digit():
    pass

def test_str():
    # 14-digit
    assert str(GTIN(raw='0123456789012')) == '01234567890128'  # str  - implicit length
    assert str(GTIN(raw='0123456789012', length=14)) == '01234567890128'  # str - explicit length
    assert str(GTIN(raw=123456789012)) == '01234567890128'  # int - implicit length
    assert str(GTIN(raw=123456789012, length=14)) == '01234567890128'  # int - explicit length
    assert str(GTIN(raw=123456789012.0)) == '01234567890128'  # float - implicit length
    assert str(GTIN(raw=123456789012.0, length=14)) == '01234567890128'  # float - explicit length
    assert str(GTIN(raw=Decimal(123456789012))) == '01234567890128'  # Decimal - implicit length
    assert str(GTIN(raw=Decimal(123456789012), length=14)) == '01234567890128'  # Decimal - explicit length
    assert str(GTIN(GTIN('01234567890128'))) == '01234567890128'  # GTIN
    # 12-digit
    assert str(GTIN(raw='01234567890')) == '012345678905'  # str - implicit length
    assert str(GTIN(raw='01234567890',length=12)) == '012345678905'  # str - explicit length
    assert str(GTIN(raw=1234567890,length=12)) == '012345678905'  # int
    assert str(GTIN(raw=1234567890.0, length=12)) == '012345678905'  # float
    assert str(GTIN(raw=Decimal(1234567890), length=12)) == '01234567890128' # Decimal
    assert str(GTIN(GTIN('01234567890128'))) == '01234567890128'
    assert str(GTIN(GTIN('01234567890128'), length=12)) == '01234567890128'


def test_gcp(self):
    pass

if __name__ == '__main__':
    print(str(GTIN(GTIN('01234567890128'), length=12)))
    #print(GTIN(raw=Decimal(123456789012)))
    #test_check_digit()