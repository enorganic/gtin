"""
A package for parsing GTINs ("Global Trade Item Numbers"—also known as UPC/EAN/JAN/ISBN).

See:
https://github.com/davebelais/gtin
"""

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='gepir',

    # See https://www.python.org/dev/peps/pep-0440/
    # TODO: https://packaging.python.org/en/latest/single_source_version.html
    version='0.1.1',

    description='A module for parsing GTINs ("Global Trade Item Numbers"—also known as UPC/EAN/JAN/ISBN).',
    long_description=long_description,

    # The project's main homepage.
    url='https://github.com/davebelais/gtin',

    # Author details
    author='David Belais',
    author_email='davebelais@gmail.com',

    # Choose your license
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        # 'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        # 'Programming Language :: Python :: 2.7',
        # 'Programming Language :: Python :: 3',
        # 'Programming Language :: Python :: 3.2',
        # 'Programming Language :: Python :: 3.3',
        # 'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    keywords='upc ean jan isbn gs1',

    packages=find_packages(exclude=['docs', 'tests']),
    # packages=[], # explicitly set packages
    # py_modules=[], # Single-file module names

    # See https://packaging.python.org/en/latest/requirements.html
    install_requires=[],

    # pip install -e .[dev,test]
    extras_require={
        'dev': [],
        'test': [],
    },

    package_data={
        'gepir': ['gcp/*.xml'],
    },

    # See http://docs.python.org/3.5/distutils/setupscript.html#installing-additional-files
    data_files=[],

    entry_points={},
)