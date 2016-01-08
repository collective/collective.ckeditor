.PHONY: checkout build build_all plone moono clean

build_all: checkout scayt plone build moono image2

checkout:
	./checkout.sh

scayt:
	./scayt.sh

plone:
	./plone.sh

build:
	./build.sh

moono:
	./moono.sh

image2:
	./image2.sh

clean:
	rm -rf ckeditor-dev download
