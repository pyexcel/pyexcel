try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

with open("README.rst", 'r') as readme:
    README_txt = readme.read()

setup(
    name='pyexcel',
    author="C. W.",
    version='0.0.5',
    author_email="wangc_2011@hotmail.com",
    url="https://github.com/chfw/pyexcel",
    description='A wrapper library to read, manipulate and write data in different excel formats: csv, ods, xls, xlsx and xlsm.',
    install_requires=[
        'six',
        'xlrd',
        'xlwt-future'
    ],
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    long_description=README_txt,
    zip_safe=False,
    tests_require=['nose'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Office/Business',
        'Topic :: Utilities',
        'Topic :: Software Development :: Libraries',
        'Programming Language :: Python',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: PyPy'
    ]
)
