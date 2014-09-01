try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='pyexcel',
    author="C. W.",
    version='0.0.1',
    url="https://github.com/chfw/pyexcel",
    description='Python Wrapper for reading uniform distributed data table in csv, ods, xls, and xlsx files',
    install_requires=[
        'xlrd',
        'openpyxl',
        'odfpy'
    ],
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False
)
