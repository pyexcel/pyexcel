cd tests\test_plugin
python setup.py install
cd ..\..\

pip freeze
nosetests --with-cov --cover-package pyexcel --cover-package tests --with-doctest --doctest-extension=.rst tests README.rst pyexcel
del tmp.db
