from decimal import Decimal

from pytest import fixture

from gtin import GTIN, GCPNotFoundError
from gtin.gcp import prefixes_lengths


@fixture
def gcp_prefixes_lengths():
    return prefixes_lengths()


def test_check_digit():
    assert GTIN(raw=890123456789).check_digit == '0'
    assert GTIN(raw=10101).check_digit == '1'
    assert GTIN(raw=567898901234).check_digit == '2'
    assert GTIN(raw=82957399425).check_digit == '3'
    assert GTIN(raw=5936663101).check_digit == '4'
    assert GTIN(raw=15059928976).check_digit == '5'
    assert GTIN(raw=901234567890).check_digit == '6'
    assert GTIN(raw=36013101).check_digit == '7'
    assert GTIN(raw=123456789012).check_digit == '8'
    assert GTIN(raw=208957399425).check_digit == '9'


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
    assert str(GTIN(raw='01234567890', length=12)) == '012345678905'  # str - explicit length
    assert str(GTIN(raw=1234567890, length=12)) == '012345678905'  # int
    assert str(GTIN(raw=1234567890.0, length=12)) == '012345678905'  # float
    assert str(GTIN(raw=Decimal(1234567890), length=12)) == '012345678905'  # Decimal
    assert str(GTIN(GTIN('01234567890128'))) == '01234567890128'
    assert str(GTIN(GTIN('01234567890128'), length=12)) == '01234567890128'
    # 8-digit
    assert str(GTIN(raw='0123456')) == '01234565'  # str - implicit length
    assert str(GTIN(raw='0123456', length=8)) == '01234565'  # str - explicit length
    assert str(GTIN(raw=123456, length=8)) == '01234565'  # int
    assert str(GTIN(raw=123456.0, length=8)) == '01234565'  # float
    assert str(GTIN(raw=Decimal(123456), length=8)) == '01234565'  # Decimal
    assert str(GTIN(GTIN('01234565'))) == '01234565'
    assert str(GTIN(GTIN('01234565'), length=8)) == '01234565'


def test_gcp(gcp_prefixes_lengths):
    # GS1 US
    assert gcp_prefixes_lengths['03321'] == 6
    assert GTIN('00332100000001').gcp == '033210'
    assert gcp_prefixes_lengths['081'] == 9
    # Restricted distribution
    assert gcp_prefixes_lengths['02'] == 0
    assert GTIN('02345678901289').gcp == ''
    assert gcp_prefixes_lengths['2'] == 0
    assert GTIN('00234567890129').gcp == ''
    # Exception handling
    gcp_not_found_error = None
    try:
        g = GTIN('01345678901280').gcp
    except Exception as e:
        gcp_not_found_error = e
    assert isinstance(gcp_not_found_error, GCPNotFoundError)


if __name__ == '__main__':
    test_check_digit()
    test_str()
    test_gcp(gcp_prefixes_lengths())
