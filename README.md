# gtin

A library and CLI for parsing and validating GTINs ("Global Trade
Item Numbers"—also known as UPC/EAN/JAN/ISBN).

## Installation

### Basic Installation

```shell
pip3 install gtin
```

### Development Installation

To install for development of *this project*:

```shell
git clone https://github.com/enorganic/gtin.git && \
cd gtin && \
make && \
source venv/bin/activate
```

## Usage

This package can be used as a CLI (command-line-interface) or library.

Please see the [Notes Concerning GCP](#notes-concerning-gcp) if calculating
a correct GCP is important to your usage.

### CLI

#### gtin ccd | gtin calculate-check-digit

```shell
$ gtin ccd -h
usage: gtin calculate-check-digit [-h] GTIN
       gtin ccd [-h] GTIN

positional arguments:
  GTIN        A GTIN without the check-digit

optional arguments:
  -h, --help  show this help message and exit
```

#### gtin acd | gtin append-check-digit

```shell
$ gtin acd -h
usage: gtin append-check-digit [-h] [-l LENGTH] GTIN
       gtin acd [-h] [-l LENGTH] GTIN

positional arguments:
  GTIN                  A GTIN without the check-digit

optional arguments:
  -h, --help            show this help message and exit
  -l LENGTH, --length LENGTH
                        The length of GTIN to return
```

#### gtin vcd | gtin validate-check-digit

```shell
$ gtin vcd -h
usage: gtin validate-check-digit [-h] GTIN
       gtin vcd [-h] GTIN

If the provided GTIN is *invalid*, this command will terminate with a non-zero
exit status.

positional arguments:
  GTIN        A GTIN *with* check-digit

optional arguments:
  -h, --help  show this help message and exit
```

#### gtin hvcd | gtin has-valid-check-digit

```shell
$ gtin hvcd -h
usage: gtin has-valid-check-digit [-h] GTIN
       gtin hvcd [-h] GTIN

If the provided GTIN is *valid*, this command will return "YES". If the
provided GTIN is *invalid*, this command will return "NO".

positional arguments:
  GTIN        A GTIN *with* check-digit

optional arguments:
  -h, --help  show this help message and exit
```

#### gtin gcp | gtin get-gcp

```shell
$ gtin gcp -h
usage: gtin get-gcp [-h] GTIN
       gtin gcp [-h] GTIN

positional arguments:
  GTIN        A GTIN *with* check-digit

optional arguments:
  -h, --help  show this help message and exit
```

### Library

#### gtin.calculate_check_digit

This function accepts a GTIN *without* check-digit and returns the check-digit.

Parameters:

- unchecked_gtin (str|int): A GTIN *without* check-digit

Note: If the provided `unchecked_gtin` is a `str`, the returned value is a
`str`. If the provided `unchecked_gtin` is an `int`, the returned value is an
`int`.

Example:

```python
>>> from gtin import calculate_check_digit
... calculate_check_digit("02345678901289")
'4'
>>> calculate_check_digit(2345678901289)
4
```

#### gtin.append_check_digit

This function accepts a GTIN *without* check-digit and returns the same
GTIN with a check-digit appended.

Note: If the provided `unchecked_gtin` is a `str`, the returned value is a
`str`. If the provided `unchecked_gtin` is an `int`, the returned value is an
`int`.

Parameters:

- unchecked_gtin (str|int): A GTIN *without* check-digit

Example:

```python
>>> from gtin import append_check_digit
... append_check_digit("02345678901289")
'023456789012894'
>>> append_check_digit(2345678901289)
23456789012894
```

#### gtin.has_valid_check_digit

This function accepts a GTIN *with* check-digit and returns `True` if the
check-digit is valid, or `False` if the check-digit is invalid.

```python
>>> from gtin import has_valid_check_digit
... has_valid_check_digit("02345678901289")
True
>>> has_valid_check_digit(2345678901281)
False
23456789012894
```

#### gtin.validate_check_digit

This function accepts a GTIN *with* check-digit and raises a
`gtin.CheckDigitError` if the provided GTIN's check-digit is invalid.

```python
>>> from gtin import validate_check_digit
... validate_check_digit("02345678901289")
>>> validate_check_digit("02345678901281")
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/Users/David/Code/gtin/gtin/__init__.py", line 159, in validate_check_digit
    raise CheckDigitError(gtin, check_digit)
gtin.CheckDigitError: "02345678901281" is not a valid GTIN, the last digit is "1", whereas the correct check-digit would be "9".
```

#### gtin.get_gcp

This function accepts a GTIN *with check-digit* and returns the GCP
(GS1 Company Prefix).

```python
>>> from gtin import get_gcp
... get_gcp("00332100000001")
'033210'
>>> get_gcp(332100000001)
'033210'
```

#### gtin.GTIN

This class represents a Global Trade Item Number, and can be used to:

- Identify a trade item's Indicator-Digit, GCP (GS1 Company Prefix),
  Item Reference, and Check-Digit.
- Validate a GTIN's check-digit.
- Calculate a check-digit from a raw GTIN.

**Parameters**:

- **gtin** (str|int): A string or number representing a GTIN, including the
  check-digit.

  - When the *gtin* parameter is provided, the last (rightmost) digit is used
    to validate the GTIN.

- **length** (int):

    The length of the GTIN.

    - If no value is provided for *length*, and *gtin* is a *str*—*length* is
      inferred based on the character length of *gtin*.
    - If no value is passed for *length*, *gtin* is *None*, and *raw* is a
      *str*—*length* is inferred based
      on the length of *raw* (adding 1, to account for the absent check-digit).
    - If no length is passed, and none can be inferred from *gtin* or *raw*,
      *length* defaults to 14.

- **raw** (str|int):

    A string or number representing the GTIN, excluding the check-digit.

    - If a value is provided for the parameter *gtin*, this parameter is not
      used, but is instead derived from *gtin*.

An instance of `GTIN` has the following properties:

- **indicator_digit** (str): This is the first (leftmost) digit of a GTIN-14.

  - "0" indicates a base unit.
  - "1" through "8" are used to define the packaging hierarchy of a product
    with the same item reference.
  - "9" indicates a variable-measure trade item.

- **gcp** (str): The GCP (GS1 Company Prefix) is a globally unique identifier
  assigned to an entity (usually a company) by GS1 Member Organizations, in
  order to create identifiers within the GS1 System. Company Prefixes, which
  vary in length, are comprised of a GS1 Member Organization Prefix followed by
  a company/entity-specific number.

- **item_reference** (str): The item reference is the part of the GTIN that is
  allocated by a GS1 entity to identify a trade item. An item reference varies
  in length as a function of a GTIN's GCP length.

- **check_digit** (str): The last digit in the GTIN when cast as a `str`, the
  check-digit is a mod-10 algorithm digit used to check for input
  errors. To understand how this digit is calculated, refer to:
  http://www.gs1.org/how-calculate-check-digit-manually.
    
- **length** (int): The number of characters comprising the GTIN
  (*including* the check-digit).

##### Examples

A *GTIN* initialized without any arguments:

```python
>>> from gtin import GTIN
... print(repr(GTIN()))
gtin.GTIN("00000000000000")
```

Typical usage will require converting your *GTIN* to a *str* prior to use in
your application.

```python
>>> from gtin import GTIN
... print(str(GTIN()))
00000000000000
```

Given a raw GTIN, the check-digit is calculated and appended.

```python
>>> from gtin import GTIN
... print(str(GTIN(raw="0978289450809")))
09782894508091
```

Given a valid GTIN *str* for *gtin*, the return value of *str(GTIN(gtin))* is
equal to *gtin*.

```python
>>> from gtin import GTIN
... print(str(GTIN("04000101613600")))
04000101613600
```

Non-numeric characters are ignored/discarded.

```python
>>> from gtin import GTIN
... print(str(GTIN("0-4000101-6136-00")))
04000101613600
```

Given a an *int* for the parameter *raw*, the length defaults to 14.

```python
>>> from gtin import GTIN
... print(str(GTIN(raw=7447010150)))
00074470101505

>>> print(str(GTIN(74470101505)))
00074470101505
```

Given a GTIN, and a length:

```python
>>> from gtin import GTIN
... print(str(GTIN(raw=7447010150,length=12)))
074470101505

>>> print(str(GTIN(74470101505,length=12)))
074470101505

>>> from gtin import GTIN
... print(str(GTIN("74470101505",length=14)))
00074470101505

```

Get the GCP of a GTIN:

```python
>>> from gtin import GTIN
... print(GTIN("00041333704647").gcp)
0041333

>>> print(GTIN("00811068011972").gcp)
081106801

>>> from gtin import GTIN
... print(GTIN("00188781000171").gcp)
0188781000
```

Get the component parts of a *GTIN* instance as a tuple containing
*GTIN.indicator_digit*, *GTIN.gcp*, *GTIN.item_reference*, and *GTIN.check_digit*:

```python
>>> from gtin import GTIN
... print(tuple(GTIN(raw="0400010161360")))
("0", "4000101", "61360", "0")
```

## Testing

Assuming you have already followed the
[Development Installation](#developmentinstallation) instructions, you can
simply run `make test` in the project directory.


## Notes Concerning GCP

If inferring a correct GCP (GS1 Company Prefix) is important for your usage,
you should update this package periodically:

```shell
pip3 install --upgrade gtin
```

Why? Because GCP allocation is subject to change. When the
GS1 (the organization which governs GCP allocation) publishes a new _GCP
Prefix Format List_ (an XML document specifying GCP lengths according to
variable-length prefix blocks), a new distribution of this package is
automatically packaged and distributed to [pypi.org](https://pypi.org) _with_
the new _GCP Prefix Format List_. If you have the most recent version of this package, you will be calculating GCPs based on the most recent _GCP Prefix
Format List_.
