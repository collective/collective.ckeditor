#!/bin/bash
CKEDITOR_DEV_DIR="$(pwd)/ckeditor-dev"
BUILDONFIG="${CKEDITOR_DEV_DIR}/dev/builder/build-config.js"
# mention image2 plugin in build configuration
# so that it gets included in the distro
sed -i '/image: 1,/aimage2: 1,' "${BUILDONFIG}"
