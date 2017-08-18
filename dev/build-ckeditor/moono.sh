#!/bin/bash
: "${CKEDITOR_VERSION:?"Need to set CKEDITOR_VERSION environment variable"}"
CKEDITOR_SRC_DIR="$(pwd)/../../src/collective/ckeditor/_src"

# make download directory
DOWNLOAD_DIR="$(pwd)/download"
if [ ! -d "${DOWNLOAD_DIR}" ]; then
        mkdir "$DOWNLOAD_DIR"
fi

# compute moono color skin version
if [[ ${CKEDITOR_VERSION} == 4.4* ]]; then
        MOONO_COLOR_VERSION=1.4.1
fi
if [[ ${CKEDITOR_VERSION} == 4.5* ]]; then
        MOONO_COLOR_VERSION=4.5.1
fi
if [[ ${CKEDITOR_VERSION} == 4.6* ]]; then
        MOONO_COLOR_VERSION=4.5.1
fi
if [[ ${CKEDITOR_VERSION} == 4.7* ]]; then
        MOONO_COLOR_VERSION=4.5.1
fi
if [ -z ${MOONO_COLOR_VERSION+x} ]; then
        echo "version of Monoo color skin could not be computed"
        exit 1
fi
MOONO_COLOR_FILE=moonocolor_${MOONO_COLOR_VERSION}.zip
MOONO_COLOR_URL=http://download.ckeditor.com/moonocolor/releases/${MOONO_COLOR_FILE}

function error_exit
{
	echo "${PROGNAME}: ${1:-"Unknown Error"}" 1>&2
	exit 1
}

echo "Downloading ${MOONO_COLOR_URL}..."
curl -o "${DOWNLOAD_DIR}/${MOONO_COLOR_FILE}" ${MOONO_COLOR_URL} || error_exit "download of Monoo Color failed" 
unzip "${DOWNLOAD_DIR}/${MOONO_COLOR_FILE}" -d "${CKEDITOR_SRC_DIR}/ckeditor/skins"
# remove standard skins
rm -rf  "${CKEDITOR_SRC_DIR}/ckeditor/skins/moono"
rm -rf  "${CKEDITOR_SRC_DIR}/ckeditor/skins/kama"
