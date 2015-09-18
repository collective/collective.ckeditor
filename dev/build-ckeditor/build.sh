#!/bin/bash
CKEDITOR_BUILDER_DIR="$(pwd)/ckeditor-dev/dev/builder"
: "${CKEDITOR_VERSION:?"Need to set CKEDITOR_VERSION environment variable"}"
"${CKEDITOR_BUILDER_DIR}/build.sh"
CKEDITOR_SRC_DIR="$(pwd)/../../src/collective/ckeditor/_src"
rm -rf "${CKEDITOR_SRC_DIR}/ckeditor"
tar -xzf "${CKEDITOR_BUILDER_DIR}/release/ckeditor_${CKEDITOR_VERSION}.tar.gz" \
    -C "${CKEDITOR_SRC_DIR}"
