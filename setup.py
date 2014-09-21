"""
    pyexcel
    ~~~~~~~~~~~~~~

    It was created due to the lack of uniform programming interface to access data in different excel formats. A developer needs to use different methods of different libraries to read the same data in different excel formats, hence the resulting code is cluttered and unmaintainable.

    All great work have done by odf, xlrd and other individual developers. This library unites only the data access code.
"""

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='pyexcel',
    author="C. W.",
    version='0.0.2',
    author_email="wangc_2011@hotmail.com",
    url="https://github.com/chfw/pyexcel",
    description='A wrapper library to read, manipulate and write data in different excel formats: csv, ods, xls, xlsx and xlsm.',
    install_requires=[
        'xlrd',
        'odfpy',
        'xlwt'
    ],
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    long_description=__doc__,
    zip_safe=False,
    tests_require=['nose'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Topic :: Office/Business',
        'Topic :: Utilities',
        'Topic :: Software Development :: Libraries',
        'Programming Language :: Python',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7'
    ]
)
