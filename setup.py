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
    description='spreadsheet wrapper',
    url='',
    install_requires=[
        'xlrd',
        'openpyxl'
    ],
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    namespace_packages=['pyexcel'],
    zip_safe=False
)
