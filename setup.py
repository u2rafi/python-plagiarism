#!/usr/bin/env python

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click', 'scikit-learn', 'flask', 'beautifulsoup4']

test_requirements = ['pytest>=3', ]

setup(
    author="Rokibul Islam",
    author_email='rafi.promit@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="A python package to detect plagiarism in document",
    entry_points={
        'console_scripts': [
            'plag=plagiarism.cli:main',
            'plagiarize=plagiarism.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,

    keywords='plagiarism',
    name='plagiarism',
    packages=find_packages(),
    package_data = {'': ['dataset/*', 'templates/*'], 'web': ['web/templates/*']},
    include_package_data=True,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/u2rafi/python-plagiarism',
    version='0.1.0',
    zip_safe=False,
)
