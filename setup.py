try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

with open("README.rst", 'r') as readme:
    README_txt = readme.read()

dependencies = [
    'pyexcel-io>=0.1.0',
    'texttable>=0.8.2',
]

extras = {
    'xls': ['pyexcel-xls>=0.1.0'],
    'xlsx': ['pyexcel-xlsx>=0.1.0'],
    'ods': ['pyexcel-ods3>=0.1.0'],
}


setup(
    name='pyexcel',
    author='C. W.',
    version='0.2.1',
    author_email='wangc_2011 (at) hotmail.com',
    url='https://github.com/pyexcel/pyexcel',
    description='A wrapper library that provides one API to read, manipulate and write data in different excel formats',
    install_requires=dependencies,
    extras_require=extras,
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    long_description=README_txt,
    zip_safe=False,
    tests_require=['nose'],
    keywords=[
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
    ],
    license='New BSD',
    classifiers=[
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
)