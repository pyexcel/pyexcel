pip install flake8
flake8 . --exclude=.moban.d,docs,setup.py --builtins=unicode,xrange,long
python setup.py checkdocs
