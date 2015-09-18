.PHONY: checkout build build_all plone moono clean


checkout:
	./checkout.sh

build:
	./build.sh

plone:
	./plone.sh

moono:
	./moono.sh

build_all: checkout plone build moono

clean:
	rm -rf ckeditor-dev moono
