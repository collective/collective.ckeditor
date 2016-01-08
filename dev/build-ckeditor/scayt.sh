#!/bin/bash
: "${CKEDITOR_VERSION:?"Need to set CKEDITOR_VERSION environment variable"}"
PLUGINS_DIR="$(pwd)/ckeditor-dev/plugins"

# make download directory
DOWNLOAD_DIR="$(pwd)/download"
if [ ! -d "${DOWNLOAD_DIR}" ]; then
        mkdir "$DOWNLOAD_DIR"
fi

# compute scayt plugin version
if [[ ${CKEDITOR_VERSION} == 4.4* ]]; then
        SCAYT_VERSION=4.4.8
fi
if [[ ${CKEDITOR_VERSION} == 4.5* ]]; then
        SCAYT_VERSION=${CKEDITOR_VERSION}
fi
if [ -z "${SCAYT_VERSION+x}" ]; then
        echo "version of scayt plugin could not be computed"
        exit 1
fi
SCAYT_FILE=scayt_${SCAYT_VERSION}.zip
SCAYT_URL=http://download.ckeditor.com/scayt/releases/${SCAYT_FILE}

# compute wsc plugin version
if [[ ${CKEDITOR_VERSION} == 4.4* ]]; then
        WSC_VERSION=4.4.8
fi
if [[ ${CKEDITOR_VERSION} == 4.5* ]]; then
        WSC_VERSION=${CKEDITOR_VERSION}
fi
if [ -z "${WSC_VERSION+x}" ]; then
        echo "version of wsc plugin could not be computed"
        exit 1
fi
WSC_FILE=wsc_${WSC_VERSION}.zip
WSC_URL=http://download.ckeditor.com/wsc/releases/${WSC_FILE}

function error_exit
{
	echo "${PROGNAME}: ${1:-"Unknown Error"}" 1>&2
	exit 1
}

echo "Downloading ${SCAYT_URL}..."
curl -o "${DOWNLOAD_DIR}/${SCAYT_FILE}" ${SCAYT_URL} || error_exit "download of scayt failed" 
unzip "${DOWNLOAD_DIR}/${SCAYT_FILE}" -d "${PLUGINS_DIR}"

echo "Downloading ${WSC_URL}..."
curl -o "${DOWNLOAD_DIR}/${WSC_FILE}" ${WSC_URL} || error_exit "download of wsc failed" 
unzip "${DOWNLOAD_DIR}/${WSC_FILE}" -d "${PLUGINS_DIR}"
