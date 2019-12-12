from decimal import Decimal

from gtin import GTIN
from gtin.gcp import GCP_PREFIXES


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
    # str  - implicit length
    assert str(GTIN(raw='0123456789012')) == '01234567890128'
    # str - explicit length
    assert str(GTIN(raw='0123456789012', length=14)) == '01234567890128'
    # int - implicit length
    assert str(GTIN(raw=123456789012)) == '01234567890128'
    # int - explicit length
    assert str(GTIN(raw=123456789012, length=14)) == '01234567890128'

    # 12-digit
    # str - implicit length
    assert str(GTIN(raw='01234567890')) == '012345678905'
    # str - explicit length
    assert str(GTIN(raw='01234567890', length=12)) == '012345678905'
    # int
    assert str(GTIN(raw=1234567890, length=12)) == '012345678905'

    # 8-digit
    # str - implicit length
    assert str(GTIN(raw='0123456')) == '01234565'
    # str - explicit length
    assert str(GTIN(raw='0123456', length=8)) == '01234565'
    # int
    assert str(GTIN(raw=123456, length=8)) == '01234565'

    # Verify that an invalid type throws an error
    error = None
    # float - implicit length
    try:
        str(GTIN(raw=123456789012.0)) == '01234567890128'
    except TypeError as e:
        error = e
    assert isinstance(error, TypeError)


def test_gcp():
    # GS1 US
    assert GCP_PREFIXES['03321'] == 6
    assert GTIN('00332100000001').gcp == '033210'
    assert GCP_PREFIXES['0810000'] == 9
    # Restricted distribution
    assert '2' not in GCP_PREFIXES
    assert '02' not in GCP_PREFIXES
    # Test restricted distribution GCPs
    assert GTIN('02345678901289').gcp == ''
    assert GTIN('00234567890129').gcp == ''
    # Test a missing GCP
    assert GTIN('01345678901280').gcp == ''
    # Test refreshing XML
    GCP_PREFIXES.refresh()


if __name__ == '__main__':
    test_check_digit()
    test_str()
    test_gcp()
