from os import environ
from sys import path
from os.path import dirname, abspath, join
from shutil import copy2

d = dirname(abspath(__file__))
pd = dirname(d)

path.insert(0,pd)
import gtin

copy2(
    join(pd,'README.rst'),
    join(d,'index.rst')
)

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.viewcode',
]
source_suffix = '.rst'
master_doc = 'index'
project = 'gtin'
copyright = '2016, David Belais'
author = 'David Belais'
release = gtin.__version__
language = None
exclude_patterns = ['_build']
pygments_style = 'sphinx'
todo_include_todos = False
if environ.get('READTHEDOCS', None) == 'True':
    html_theme = 'default'
else:
    html_theme = 'nature'
html_static_path = ['_static']
htmlhelp_basename = 'gtindoc'
latex_documents = [
    (master_doc, 'gtin.tex', 'gtin Documentation',
     'David Belais', 'manual'),
]
man_pages = [
    (master_doc, 'gtin', 'gtin Documentation',
     [author], 1)
]
texinfo_documents = [
    (master_doc, 'gtin', 'gtin Documentation',
     author, 'gtin', 'One line description of project.',
     'Miscellaneous'),
]