all: test

test:
	bash test.sh

doc:
	bash document.sh

uml:
	plantuml -tsvg -o ../_static/images/ docs/source/uml/*.uml
