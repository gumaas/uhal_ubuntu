#!/bin/bash

export API_DIR=/afs/cern.ch/user/c/cactus/www/nightly/api
export BUILD_HOME=/build/cactus/cactus
 
rm -rf $API_DIR
mkdir -p $API_DIR

cd $BUILD_HOME/trunk/scripts/nightly
doxygen Doxyfile
cp -rf html $API_DIR/.
