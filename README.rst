gtin
=========

A library for parsing GTINs ("Global Trade Item Numbers"—also known as UPC/EAN/JAN/ISBN).

gtin.GTIN
---------

This class represents a Global Trade Item Number, and can be used to:

- Identify a trade item's GCP (GS1 Company Prefix), Item Reference, and Indicator Digit.
- Validate a GTIN's check-digit.
- Calculate a check-digit from a raw GTIN.

Typical usage will require converting your `GTIN` to a `str` prior to use in your application:

>>> print(repr(GTIN()))
GTIN('00000000000000')

>>> print(str(GTIN()))
00000000000000

Given a raw gtin, the check-digit is calculated and appended.

>>> print(str(GTIN(raw='0978289450809')))
09782894508091

Given a valid gtin as a string, the `GTIN.__str__` output is the same as the GTIN provided.

>>> print(str(GTIN('04000101613600')))
04000101613600

Given a GTIN as an integer, the length defaults to 14.

>>> print(str(GTIN(raw=7447010150)))
00074470101505

>>> print(str(GTIN(74470101505)))
00074470101505

Given a GTIN, and a length:

>>> print(str(GTIN(raw=7447010150,length=12)))
074470101505

>>> print(str(GTIN(74470101505,length=12)))
074470101505

>>> print(str(GTIN('74470101505',length=14)))
00074470101505

Get the GCP of a GTIN:

>>> print(GTIN('00041333704647').gcp)
0041333

>>> print(GTIN('00811068011972').gcp)
081106801

>>> print(GTIN('00188781000171').gcp)
0188781000

Get the component parts of the GTIN as a tuple
(`GTIN.indicator_digit`, `GTIN.gcp`, `GTIN.item_reference`, `GTIN.check_digit`).

>>> print(tuple(GTIN(raw='0400010161360')))
('0', '4000101', '61360', '0')