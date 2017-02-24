#!/bin/bash
: "${CKEDITOR_VERSION:?"Need to set CKEDITOR_VERSION environment variable"}"
CKEDITOR_SRC_DIR="$(pwd)/../../src/collective/ckeditor/_src"

# make download directory
DOWNLOAD_DIR="$(pwd)/download"
if [ ! -d "${DOWNLOAD_DIR}" ]; then
        mkdir "$DOWNLOAD_DIR"
fi

# compute image2 plugin version
if [[ ${CKEDITOR_VERSION} == 4.4* ]]; then
        IMAGE2_VERSION=4.4.8
fi
if [[ ${CKEDITOR_VERSION} == 4.5* ]]; then
        IMAGE2_VERSION=4.5.11
fi
if [[ ${CKEDITOR_VERSION} == 4.6* ]]; then
        IMAGE2_VERSION=${CKEDITOR_VERSION}
fi
if [ -z "${IMAGE2_VERSION+x}" ]; then
        echo "version of image2 plugin could not be computed"
        exit 1
fi
IMAGE2_FILE=image2_${IMAGE2_VERSION}.zip
IMAGE2_URL=http://download.ckeditor.com/image2/releases/${IMAGE2_FILE}

function error_exit
{
	echo "${PROGNAME}: ${1:-"Unknown Error"}" 1>&2
	exit 1
}

echo "Downloading ${IMAGE2_URL}..."
curl -o "${DOWNLOAD_DIR}/${IMAGE2_FILE}" "${IMAGE2_URL}" || error_exit "download of image2 failed" 
rm -rf "${CKEDITOR_SRC_DIR}/ckeditor/plugins/image2"
unzip "${DOWNLOAD_DIR}/${IMAGE2_FILE}" -d "${CKEDITOR_SRC_DIR}/ckeditor/plugins"
