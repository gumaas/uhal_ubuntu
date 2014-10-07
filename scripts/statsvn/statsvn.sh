#!/bin/bash

TMP_DIR=/tmp/generate_stats
STATSVN_DIR=$HOME/statsvn
RESULT_DIR=/afs/cern.ch/user/c/cactus/www/statsvn

#Clean and create directories
rm -rf $TMP_DIR 
mkdir -p $TMP_DIR 
rm -rf $RESULT_DIR
mkdir -p $RESULT_DIR

#Checkout
rm -rf $TMP_DIR 
mkdir -p $TMP_DIR 
cd $TMP_DIR 
svn co svn+ssh://svn.cern.ch/reps/cactus/trunk

#Get SVN logs
cd trunk
svn log --xml -v > $TMP_DIR/svn.log

#Generate stats
cd $RESULT_DIR
java -mx512m -jar $STATSVN_DIR/statsvn.jar -include "**/*.c;**/*.cc;**/*.cpp;**/*.c++;**/*.cxx;**/*.h;**/*.hh;**/*.h++;**/*.hxx;**/*.hpp;**/*.java;**/*.py;**/*.pl;**/*.sh;**/*.erl;**/*.hrl" $TMP_DIR/svn.log $TMP_DIR/trunk 
