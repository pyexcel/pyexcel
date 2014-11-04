all: test

test:
	bash test.sh

document:
	sphinx-autogen -o doc/source/generated/ doc/source/*.rst
	sphinx-build -b html doc/source/ doc/build/
