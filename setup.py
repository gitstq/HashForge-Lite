#!/usr/bin/env python3
"""
HashForge - Lightweight Terminal Hash, Encoding & Encryption Toolkit
"""

from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='hashforge',
    version='1.0.0',
    author='HashForge Team',
    author_email='hashforge@example.com',
    description='🔐 Lightweight Terminal Hash, Encoding & Encryption Toolkit',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/gitstq/HashForge',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Security :: Cryptography',
        'Topic :: Utilities',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.8',
    entry_points={
        'console_scripts': [
            'hashforge=hashforge.cli:main',
        ],
    },
    keywords='hash encoding encryption password cli terminal tui cryptography md5 sha256 base64',
    project_urls={
        'Bug Tracker': 'https://github.com/gitstq/HashForge/issues',
        'Documentation': 'https://github.com/gitstq/HashForge#readme',
        'Source Code': 'https://github.com/gitstq/HashForge',
    },
)
