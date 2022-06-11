#!/usr/bin/env python3

"""
Template by pypi-mobans
"""

import os
import sys
from shutil import rmtree

from setuptools import Command, setup, find_packages

NAME = "pyexcel"
AUTHOR = "C.W."
VERSION = "0.7.0"
EMAIL = "info@pyexcel.org"
LICENSE = "New BSD"
DESCRIPTION = (
    "A wrapper library that provides one API to read, manipulate and write" +
    "data in different excel formats"
)
URL = "https://github.com/pyexcel/pyexcel"
DOWNLOAD_URL = "%s/archive/0.7.0.tar.gz" % URL
README_FILES = ["README.rst", "CONTRIBUTORS.rst", "CHANGELOG.rst"]
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
    "chardet",
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
HERE = os.path.abspath(os.path.dirname(__file__))

GS_COMMAND = ("gease pyexcel v0.7.0 " +
              "Find 0.7.0 in changelog for more details")
NO_GS_MESSAGE = ("Automatic github release is disabled. " +
                 "Please install gease to enable it.")
UPLOAD_FAILED_MSG = (
    'Upload failed. please run "%s" yourself.' % PUBLISH_COMMAND)


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
    return "\n".join([read(filename) for filename in files])


def read(filename):
    """Read a file into setup"""
    filename_absolute = os.path.join(HERE, filename)

    with open(filename_absolute) as opened_file:
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
        long_description=read_files(*README_FILES),
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
        #cmdclass=SETUP_COMMANDS
    )
