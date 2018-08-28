pip freeze
nosetests --with-coverage --cover-package pyexcel --cover-package tests tests --with-doctest --doctest-extension=.rst README.rst docs/source pyexcel && flake8 . --exclude=.moban.d,docs --builtins=unicode,xrange,long
