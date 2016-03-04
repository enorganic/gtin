from os.path import dirname, abspath, join
from shutil import copy2
import gtin.__author__

d = dirname(abspath(__file__))
pd = dirname(d)

copy2(
    join(pd,'README.rst'),
    join(d,'index.rst')
)

with open(join(d,'contents.rst'),'w') as f:
    f.write('toctree::\n')

project = 'gtin'



