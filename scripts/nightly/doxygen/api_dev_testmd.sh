#!/bin/bash

export DOXYGEN_HOME=${HOME}/doxygen/doxygen-1.8.6/
export CACTUS_SANDBOX=/build/cactus/cactus/trunk
export CACTUS_SANDBOX=${HOME}/doxygen/test
export API_DIR=/afs/cern.ch/user/c/cactus/www/nightly/api
export HTML_OUT=/tmp/
export DOXYGEN_OUTPUT=/tmp/

cd ${HOME}/doxygen
echo "Cleaning up target directory"
rm -r ${HTML_OUT}/html

DOXYGEN_MAINPAGE="${CACTUS_SANDBOX}/cactuscore/uhal/README.md"
DOXYGEN_INPUTS="${CACTUS_SANDBOX}/cactuscore/uhal "

echo DOXYGEN_INPUTS=${DOXYGEN_INPUTS}
export DOXYGEN_MAINPAGE DOXYGEN_INPUTS
${DOXYGEN_HOME}/bin/doxygen cactus-v2.doxy


echo "Removing old APIs"
rm -r ${API_DIR}/html_dev_testmd

echo "Uploading..."
mkdir -p ${API_DIR}
cp -a ${HTML_OUT}/html ${API_DIR}/html_dev_testmd
echo "Done"
