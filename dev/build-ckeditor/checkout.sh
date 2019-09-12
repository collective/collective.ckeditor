#!/bin/bash
: "${CKEDITOR_VERSION:?"Need to set CKEDITOR_VERSION environment variable"}"
CKEDITOR_GITHUB_URL="git@github.com:ckeditor/ckeditor4.git"
CKEDITOR_DEV_DIR="$(pwd)/ckeditor-dev"
if [ ! -d "${CKEDITOR_DEV_DIR}" ]; then
        git clone "${CKEDITOR_GITHUB_URL}"
fi
cd "${CKEDITOR_DEV_DIR}" || exit
if [ ! -d ".git" ]; then
        echo "$(pwd) is not a git checkout"
        exit 1
fi
git fetch origin
git checkout "${CKEDITOR_VERSION}"
git checkout -- dev/builder/build-config.js
cd ..
