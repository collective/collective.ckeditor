#!/bin/bash
: "${CKEDITOR_VERSION:?"Need to set CKEDITOR_VERSION environment variable"}"

CKEDITOR_BUILDER_DIR="$(pwd)/ckeditor-dev/dev/builder"
CKEDITOR_BUILDER="${CKEDITOR_BUILDER_DIR}/build.sh"
if [ ! -f "${CKEDITOR_BUILDER}" ]; then
        echo "builder script ${CKEDITOR_BUILDER} not found"
        exit 1
fi
"${CKEDITOR_BUILDER}"

CKEDITOR_SRC_DIR="$(pwd)/../../src/collective/ckeditor/_src"
rm -rf "${CKEDITOR_SRC_DIR}/ckeditor"

CKEDITOR_RELEASE="${CKEDITOR_BUILDER_DIR}/release/ckeditor_${CKEDITOR_VERSION}.tar.gz"
if [ ! -f "${CKEDITOR_RELEASE}" ]; then
        echo "ckeditor release ${CKEDITOR_RELEASE} not found"
        exit 1
fi
tar -xzf "${CKEDITOR_RELEASE}" -C "${CKEDITOR_SRC_DIR}"
