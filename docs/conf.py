from os.path import dirname, abspath, join
from shutil import copy2

d = dirname(abspath(__file__))
pd = dirname(d)

copy2(
    join(pd,'README.rst'),
    join(d,'index.rst')
)

