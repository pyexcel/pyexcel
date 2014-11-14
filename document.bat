python setup.py install
del doc\source\generated\*.rst
del doc\source\iapi\*.rst
sphinx-autogen -o doc\source\generated doc\source\api.rst
sphinx-autogen -o doc\source\iapi doc\source\iapi.rst
sphinx-build -b html doc\source doc\build
