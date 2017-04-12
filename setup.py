try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages
from platform import python_implementation
import sys
PY2 = sys.version_info[0] == 2
PY26 = PY2 and sys.version_info[1] < 7

NAME = 'pyexcel'
AUTHOR = 'C.W.'
VERSION = '0.5.0'
EMAIL = 'wangc_2011 (at) hotmail.com'
LICENSE = 'New BSD'
DESCRIPTION = (
    'A wrapper library that provides one API to read, manipulate and write ' +
    'data in different excel formats' +
    ''
)
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

CLASSIFIERS = [
    'Topic :: Office/Business',
    'Topic :: Utilities',
    'Topic :: Software Development :: Libraries',
    'Programming Language :: Python',
    'License :: OSI Approved :: BSD License',
    'Intended Audience :: Developers',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Development Status :: 3 - Alpha',
    'Programming Language :: Python :: Implementation :: PyPy'
]

INSTALL_REQUIRES = [
    'lml',
    'pyexcel-io>=0.4.0',
]

if PY2:
    INSTALL_REQUIRES.append('texttable>=0.8.1')
if not PY2:
    INSTALL_REQUIRES.append('texttable>=0.8.2')
if PY26:
    INSTALL_REQUIRES.append('ordereddict')
if PY26:
    INSTALL_REQUIRES.append('weakrefset')
if python_implementation == "PyPy":
    INSTALL_REQUIRES.append('lxml==3.4.4')

PACKAGES = find_packages(exclude=['ez_setup', 'examples', 'tests'])
EXTRAS_REQUIRE = {
    'xls': ['pyexcel-xls>=0.3.0'],
    'xlsx': ['pyexcel-xlsx>=0.3.0'],
    'ods': ['pyexcel-ods3>=0.3.0'],
}


def read_files(*files):
    """Read files into setup"""
    text = ""
    for single_file in files:
        content = read(single_file)
        text = text + content + "\n"
    return text


def read(afile):
    """Read a file into setup"""
    with open(afile, 'r') as opened_file:
        content = filter_out_test_code(opened_file)
        content = "".join(list(content))
        return content


def filter_out_test_code(file_handle):
    found_test_code = False
    for line in file_handle.readlines():
        if line.startswith('.. testcode:'):
            found_test_code = True
            continue
        if found_test_code is True:
            if line.startswith('  '):
                continue
            else:
                empty_line = line.strip()
                if len(empty_line) == 0:
                    continue
                else:
                    found_test_code = False
                    yield line
        else:
            yield line


if __name__ == '__main__':
    setup(
        name=NAME,
        author=AUTHOR,
        version=VERSION,
        author_email=EMAIL,
        description=DESCRIPTION,
        long_description=read_files('README.rst', 'CHANGELOG.rst'),
        license=LICENSE,
        keywords=KEYWORDS,
        extras_require=EXTRAS_REQUIRE,
        tests_require=['nose'],
        install_requires=INSTALL_REQUIRES,
        packages=PACKAGES,
        include_package_data=True,
        zip_safe=False,
        classifiers=CLASSIFIERS
    )
