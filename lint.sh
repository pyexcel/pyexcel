pip install flake8
flake8 --exclude=.venv,.moban.d,docs,setup.py   --builtins=unicode,xrange,long .  && python setup.py checkdocs