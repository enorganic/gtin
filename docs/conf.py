import pkg_resources
from os import environ
from sys import path
from os.path import dirname, abspath, join
from shutil import copy2

d = dirname(abspath(__file__))
pd = dirname(d)

path.insert(0,pd)

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
try:
    release = pkg_resources.get_distribution('gtin').version
except pkg_resources.DistributionNotFound:
    release = '0.0.0'
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
    (
        master_doc,
        'gtin',
        'gtin Documentation',
        author,
        'gtin',
        'A python module for parsing GTINs ("Global Trade Item Numbers"—also known as UPC/EAN/JAN/ISBN).',
        'Miscellaneous'
    ),
]