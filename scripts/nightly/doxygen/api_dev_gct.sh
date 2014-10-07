#!/bin/bash

export DOXYGEN_HOME=${HOME}/doxygen/doxygen-1.8.6/
export CACTUS_SANDBOX=/build/cactus/cactus/trunk
# export CACTUS_SANDBOX=${HOME}/doxygen/test
export API_DIR=/afs/cern.ch/user/c/cactus/www/nightly/api
export DOXYGEN_OUTPUT=/tmp/api_gct/
export DOXYGEN_WWW=${API_DIR}/html_dev_gct

cd ${HOME}/nightly/doxygen
echo "Cleaning up target directory"
rm -r ${DOXYGEN_OUTPUT}/html

DOXYGEN_INPUTS="${CACTUS_SANDBOX}/cactusprojects/gct/README.md ${CACTUS_SANDBOX}/cactusprojects/gct/ "
# DOXYGEN_INPUTS+="${CACTUS_SANDBOX}/cactuscore/ts "
DOXYGEN_PROJECT_NAME='GCT Online Software (nightly)'

echo DOXYGEN_INPUTS=${DOXYGEN_INPUTS}
export DOXYGEN_MAINPAGE DOXYGEN_INPUTS DOXYGEN_PROJECT_NAME
mkdir -p ${DOXYGEN_OUTPUT}
${DOXYGEN_HOME}/bin/doxygen cactus-v2.doxy


echo "Removing old APIs"
rm -r ${API_DIR}/html_dev_gct

echo "Uploading..."
mkdir -p ${API_DIR}
cp -a ${DOXYGEN_OUTPUT}/html ${API_DIR}/html_dev_gct
echo "Done"
