"""
A python package for parsing GTINs ("Global Trade Item Numbers"—also known as UPC/EAN/JAN/ISBN).

See:
https://github.com/davebelais/gtin
"""
import re
from setuptools import setup, find_packages
from codecs import open
from os import path

d = path.abspath(path.dirname(__file__))

# Get a long description from the README file
with open(
    path.join(
        d,
        'README.md'
    ),
    encoding='utf-8'
) as f:
    long_description = ''.join(
        re.split(
            r'(^\s*To\s*install::\s*$)',
            f.read(),
            flags=re.IGNORECASE+re.MULTILINE
        )[1:]
    )

setup(
    name='gtin',
    version="0.1.13",
    description=(
        'A module for parsing GTINs ("Global Trade Item Numbers"--also '
        'known as UPC/EAN/JAN/ISBN).'
    ),
    long_description=long_description,
    url='https://github.com/davebelais/gtin',
    # Author details,
    author='David Belais',
    author_email='david@belais.me',
    license='MIT',
    python_requires='>=2.7',
    keywords='upc ean jan isbn gs1',
    packages=find_packages(exclude=['docs', 'tests']),
    install_requires=[
        "future>=0.18.2"
    ],
    extras_require={
        "dev": [
            "pytest>=5.1.1",
            "setuptools_setup_versions>=0.0.28"
        ],
        "test": [
            "pytest>=5.1.1",
            "setuptools_setup_versions>=0.0.28"
        ]
    },
    package_data={
        'gtin': ['gcp/*.xml'],
    },
    data_files=[],
    entry_points={
        'console_scripts': [],
    }
)