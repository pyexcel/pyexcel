#!/usr/bin/env python3

"""
Template by pypi-mobans
"""

import os
import sys
import codecs
import locale
import platform
from shutil import rmtree

from setuptools import Command, setup, find_packages

PY2 = sys.version_info[0] == 2
PY26 = PY2 and sys.version_info[1] < 7
PY33 = sys.version_info < (3, 4)

# Work around mbcs bug in distutils.
# http://bugs.python.org/issue10945
# This work around is only if a project supports Python < 3.4

# Work around for locale not being set
try:
    lc = locale.getlocale()
    pf = platform.system()
    if pf != "Windows" and lc == (None, None):
        locale.setlocale(locale.LC_ALL, "C.UTF-8")
except (ValueError, UnicodeError, locale.Error):
    locale.setlocale(locale.LC_ALL, "en_US.UTF-8")

NAME = "pyexcel"
AUTHOR = "chfw"
VERSION = "0.6.6"
EMAIL = "info@pyexcel.org"
LICENSE = "New BSD"
DESCRIPTION = (
    "A wrapper library that provides one API to read, manipulate and write" +
    "data in different excel formats"
)
URL = "https://github.com/pyexcel/pyexcel"
DOWNLOAD_URL = "%s/archive/0.6.6.tar.gz" % URL
FILES = ["README.rst", "CONTRIBUTORS.rst", "CHANGELOG.rst"]
KEYWORDS = [
    "python",
    'tsv',
    'tsvz'
    'csv',
    'csvz',
    'xls',
    'xlsx',
    'ods'
]

CLASSIFIERS = [
    "Topic :: Software Development :: Libraries",
    "Programming Language :: Python",
    "Intended Audience :: Developers",

    "Programming Language :: Python :: 3 :: Only",



    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",

    'Development Status :: 3 - Alpha',
]

PYTHON_REQUIRES = ">=3.6"

INSTALL_REQUIRES = [
    "lml>=0.0.4",
    "pyexcel-io>=0.6.2",
    "texttable>=0.8.2",
]
SETUP_COMMANDS = {}

PACKAGES = find_packages(exclude=["ez_setup", "examples", "tests", "tests.*"])
EXTRAS_REQUIRE = {
    "xls": ['pyexcel-xls>=0.6.0'],
    "xlsx": ['pyexcel-xlsx>=0.6.0'],
    "ods": ['pyexcel-ods3>=0.6.0'],
}
# You do not need to read beyond this line
PUBLISH_COMMAND = "{0} setup.py sdist bdist_wheel upload -r pypi".format(sys.executable)
GS_COMMAND = ("gs pyexcel v0.6.6 " +
              "Find 0.6.6 in changelog for more details")
NO_GS_MESSAGE = ("Automatic github release is disabled. " +
                 "Please install gease to enable it.")
UPLOAD_FAILED_MSG = (
    'Upload failed. please run "%s" yourself.' % PUBLISH_COMMAND)
HERE = os.path.abspath(os.path.dirname(__file__))


class PublishCommand(Command):
    """Support setup.py upload."""

    description = "Build and publish the package on github and pypi"
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print("\033[1m{0}\033[0m".format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status("Removing previous builds...")
            rmtree(os.path.join(HERE, "dist"))
            rmtree(os.path.join(HERE, "build"))
            rmtree(os.path.join(HERE, "pyexcel.egg-info"))
        except OSError:
            pass

        self.status("Building Source and Wheel (universal) distribution...")
        run_status = True
        if has_gease():
            run_status = os.system(GS_COMMAND) == 0
        else:
            self.status(NO_GS_MESSAGE)
        if run_status:
            if os.system(PUBLISH_COMMAND) != 0:
                self.status(UPLOAD_FAILED_MSG)

        sys.exit()


SETUP_COMMANDS.update({
    "publish": PublishCommand
})


def has_gease():
    """
    test if github release command is installed

    visit http://github.com/moremoban/gease for more info
    """
    try:
        import gease  # noqa
        return True
    except ImportError:
        return False


def read_files(*files):
    """Read files into setup"""
    text = ""
    for single_file in files:
        content = read(single_file)
        text = text + content + "\n"
    return text


def read(afile):
    """Read a file into setup"""
    the_relative_file = os.path.join(HERE, afile)
    with codecs.open(the_relative_file, "r", "utf-8") as opened_file:
        content = filter_out_test_code(opened_file)
        content = "".join(list(content))
        return content


def filter_out_test_code(file_handle):
    found_test_code = False
    for line in file_handle.readlines():
        if line.startswith(".. testcode:"):
            found_test_code = True
            continue
        if found_test_code is True:
            if line.startswith("  "):
                continue
            else:
                empty_line = line.strip()
                if len(empty_line) == 0:
                    continue
                else:
                    found_test_code = False
                    yield line
        else:
            for keyword in ["|version|", "|today|"]:
                if keyword in line:
                    break
            else:
                yield line


if __name__ == "__main__":
    setup(
        test_suite="tests",
        name=NAME,
        author=AUTHOR,
        version=VERSION,
        author_email=EMAIL,
        description=DESCRIPTION,
        url=URL,
        download_url=DOWNLOAD_URL,
        long_description=read_files(*FILES),
        license=LICENSE,
        keywords=KEYWORDS,
        python_requires=PYTHON_REQUIRES,
        extras_require=EXTRAS_REQUIRE,
        tests_require=["nose"],
        install_requires=INSTALL_REQUIRES,
        packages=PACKAGES,
        include_package_data=True,
        zip_safe=False,
        classifiers=CLASSIFIERS,
        cmdclass=SETUP_COMMANDS
    )
