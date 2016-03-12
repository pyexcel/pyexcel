python setup.py install
rm doc/source/generated/*.rst
rm doc/source/iapi/*.rst
sphinx-autogen -o doc/source/generated doc/source/api.rst
sphinx-autogen -o doc/source/iapi doc/source/iapi.rst
sphinx-build -b html doc/source doc/build
