try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

NAME = 'pyexcel'
AUTHOR = 'C.W.'
VERSION = '0.2.3'
EMAIL = 'wangc_2011 (at) hotmail.com'
LICENSE = 'New BSD'
PACKAGES = find_packages(exclude=['ez_setup', 'examples', 'tests'])
DESCRIPTION = 'A wrapper library that provides one API to read, manipulate and write data in different excel formats'
KEYWORDS = [
   'excel',
   'python',
   'pyexcel',
    'tsv',
    'tsvz'
    'csv',
    'csvz',
    'xls',
    'xlsx',
    'ods'
]

INSTALL_REQUIRES = [
    'pyexcel-io>=0.2.0',
]

EXTRAS_REQUIRE = {
    'xls': ['pyexcel-xls>=0.2.0'],
    'xlsx': ['pyexcel-xlsx>=0.2.0'],
    'ods': ['pyexcel-ods3>=0.2.0'],
  ':python_version<"3"': [
    'texttable>=0.8.1'
  ],
  ':python_version>="3"': [
    'texttable>=0.8.2'
  ],
  ':python_version<"2.7"': [
    'ordereddict'
  ],
  ':python_version<"2.7"': [
    'weakrefset'
  ],
  ':platform_python_implementation=="PyPy"': [
    'lxml==3.4.4'
  ],
}

CLASSIFIERS = [
    'Topic :: Office/Business',
    'Topic :: Utilities',
    'Topic :: Software Development :: Libraries',
    'Programming Language :: Python',
    'License :: OSI Approved :: BSD License',
    'Intended Audience :: Developers',
    'Development Status :: 3 - Alpha',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: Implementation :: PyPy'
]


def read_files(*files):
    """Read files into setup"""
    text = ""
    for single_file in files:
        text = text + read(single_file) + "\n"
    return text


def read(afile):
    """Read a file into setup"""
    with open(afile, 'r') as opened_file:
        return opened_file.read()


if __name__ == '__main__':
    setup(
        name=NAME,
        author=AUTHOR,
        version=VERSION,
        author_email=EMAIL,
        description=DESCRIPTION,
        install_requires=INSTALL_REQUIRES,
        keywords=KEYWORDS,
        extras_require=EXTRAS_REQUIRE,
        packages=PACKAGES,
        include_package_data=True,
        long_description=read_files('README.rst', 'CHANGELOG.rst'),
        zip_safe=False,
        tests_require=['nose'],
        license=LICENSE,
        classifiers=CLASSIFIERS
    )
