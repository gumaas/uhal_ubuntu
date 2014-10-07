#!/bin/bash

export DOXYGEN_HOME=${HOME}/doxygen/doxygen-1.8.6/
export CACTUS_SANDBOX=/build/cactus/cactus/trunk
# export CACTUS_SANDBOX=${HOME}/doxygen/test
export API_DIR=/afs/cern.ch/user/c/cactus/www/nightly/api
export DOXYGEN_OUTPUT=/tmp/api_swatch/
export DOXYGEN_WWW=${API_DIR}/html_dev_swatch

cd ${HOME}/nightly/doxygen
echo "Cleaning up target directory"
rm -r ${DOXYGEN_OUTPUT}/html

DOXYGEN_MAINPAGE="${CACTUS_SANDBOX}/cactuscore/swatch/README.md"
DOXYGEN_INPUTS="${CACTUS_SANDBOX}/cactuscore/swatch/ "
DOXYGEN_PROJECT_NAME='SWATCH Package (nightly)'
DOXYGEN_EXCLUDE_PATTERNS=''

echo DOXYGEN_INPUTS=${DOXYGEN_INPUTS}
export DOXYGEN_MAINPAGE DOXYGEN_INPUTS DOXYGEN_PROJECT_NAME
mkdir -p ${DOXYGEN_OUTPUT}
${DOXYGEN_HOME}/bin/doxygen cactus-v3.doxy


echo "Removing old APIs"
rm -r ${DOXYGEN_WWW}

echo "Uploading..."
mkdir -p ${API_DIR}
cp -a ${DOXYGEN_OUTPUT}/html ${DOXYGEN_WWW}
echo "Done"
