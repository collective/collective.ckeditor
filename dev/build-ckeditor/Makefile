.PHONY: checkout build build_all plone moono clean


checkout:
	./checkout.sh

build:
	./build.sh

plone:
	./plone.sh

moono:
	./moono.sh

scayt:
	./scayt.sh

build_all: checkout plone build moono scayt

clean:
	rm -rf ckeditor-dev download
